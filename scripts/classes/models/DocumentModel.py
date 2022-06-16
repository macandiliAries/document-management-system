from scripts.utilities.dbConnection import DbConnection

class DocumentModel(DbConnection):

    def getDocuments(self):
        query = """
                SELECT
                    d.id AS docId, d.title, u1.full_name AS author, dt.docType, dst.statusType AS status,
                    u2.full_name AS approver, d.effectiveDate, d.contents, d.lastEditedOn, dr.revisionNumber
                FROM
                    docs AS d
                        INNER JOIN users AS u1
                            ON d.authorId = u1.id
                        INNER JOIN doc_types AS dt
                            ON d.docTypeId = dt.id
                        INNER JOIN doc_status_types AS dst
                            ON d.statusId = dst.id
                        LEFT JOIN users AS u2
                            ON d.approverId = u2.id
                        INNER JOIN doc_revisions AS dr
                            ON d.id = dr.docId
                            AND dr.id = (
                                SELECT
                                    MAX(id)
                                FROM
                                    doc_revisions AS dr1
                                WHERE
                                    dr1.docId = d.id
                            )
                """

        query = ' '.join(query.split())
        queryResult = self._executeQuery(query, ()).fetchall()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def getDocumentDetails(self, id):
        query = """
                SELECT
                    d.id AS docId, d.title, u1.full_name AS author, dt.docType, d.contents, dst.statusType AS status,
                    u2.full_name AS lastEditedBy, d.lastEditedBy AS lastEditorId, d.lastEditedOn
                FROM
                    docs AS d
                        INNER JOIN users AS u1
                            ON d.authorId = u1.id
                        INNER JOIN doc_types AS dt
                            ON d.docTypeId = dt.id
                        INNER JOIN doc_status_types AS dst
                            ON d.statusId = dst.id
                        LEFT JOIN users AS u2
                            ON d.lastEditedBy = u2.id
                WHERE
                    d.id = %s
                """

        query = ' '.join(query.split())
        queryResult = self._executeQuery(query, (id,)).fetchone()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def createNewDocument(self, columns: tuple, queryParams: tuple):
        query = "INSERT INTO docs (" + ', '.join(columns) + ") VALUES " + self._generatePlaceHolders(columns)
        self._executeQuery(query, queryParams)
        self._commitChanges()
        return self._getLastRowId()

    def updateExistingDocument(self, queryParams: dict):
        setParams = ', '.join('{} = ?'.format(setKey) for setKey in queryParams['set'].keys())
        whereParams = ' AND '.join('{} = ?'.format(whereKey) for whereKey in queryParams['where'].keys())
        query = "UPDATE docs SET {} WHERE {}".format(setParams, whereParams)
        queryParams = tuple(list(queryParams['set'].values()) + list(queryParams['where'].values()))
        self._executeQuery(query, queryParams)
        self._commitChanges()
        return self._getAffectedRows()

    def deleteDocument(self, id: int):
        query = "DELETE FROM docs WHERE id = %s"
        self._executeQuery(query, (id,))
        self._commitChanges()
        return self._getAffectedRows()
from scripts.utilities.dbConnection import DbConnection

class DocumentRevisionModel(DbConnection):

    def getDocumentRevisions(self, id):
        query = """
                SELECT
                    dr.id AS revisionId, dr.revisionNumber, dr.dateRevised, dr.significantChanges, u.full_name AS revisedBy, dr.isApproved
                FROM
                    doc_revisions AS dr
                        LEFT JOIN users AS u
                            ON dr.reviserId = u.id
                WHERE
                    dr.docId = %s
                ORDER BY
                    dr.dateRevised DESC
                """

        query = ' '.join(query.split())
        queryResult = self._executeQuery(query, (id,)).fetchall()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def insertDocumentRevision(self, columns: tuple, queryParams: tuple):
        query = "INSERT INTO doc_revisions (" + ', '.join(columns) + ") VALUES " + self._generatePlaceHolders(columns)
        self._executeQuery(query, queryParams)
        self._commitChanges()
        return self._getAffectedRows()

    def deleteDocumentRevision(self, id: int):
        query = "DELETE FROM doc_revisions WHERE id = %s"
        self._executeQuery(query, (id,))
        self._commitChanges()
        return self._getAffectedRows()

    def updateDocumentRevision(self, queryParams: dict):
        setParams = ', '.join('{} = ?'.format(setKey) for setKey in queryParams['set'].keys())
        whereParams = ' AND '.join('{} = ?'.format(whereKey) for whereKey in queryParams['where'].keys())
        query = "UPDATE doc_revisions SET {} WHERE {}".format(setParams, whereParams)
        queryParams = tuple(list(queryParams['set'].values()) + list(queryParams['where'].values()))
        self._executeQuery(query, queryParams)
        self._commitChanges()
        return self._getAffectedRows()

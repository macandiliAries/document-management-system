from scripts.utilities.dbConnection import DbConnection

class DocumentStatusTypeModel(DbConnection):

    def getSubmissionReviewStatus(self, docId):
        query = """
                SELECT
                    CASE
                        WHEN dst.statusType = "Draft"
                            THEN 2 /* "For Review" */
                        ELSE
                            5 /* "For Revision Review" */
                    END AS statusId
                FROM
                    doc_status_types AS dst
                        INNER JOIN docs AS d
                            ON dst.id = d.statusId
                WHERE
                    d.id = %s
                """

        query = ' '.join(query.split())
        queryResult = self._executeQuery(query, (docId,)).fetchone()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def getRejectStatus(self, docId):
        query = """
                SELECT
                    CASE
                        WHEN dst.statusType = "For Review"
                            THEN 1 /* "Draft" */
                        ELSE
                            6 /* "Draft Revision" */
                    END AS statusId
                FROM
                    doc_status_types AS dst
                        INNER JOIN docs AS d
                            ON dst.id = d.statusId
                WHERE
                    d.id = %s
                """

        query = ' '.join(query.split())
        queryResult = self._executeQuery(query, (docId,)).fetchone()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def getDraftStatus(self, docId):
        query = """
                SELECT
                    CASE
                        WHEN dst.statusType IN ("For Revision", "Draft Revision")
                            THEN 6 /* "Draft Revision" */
                        ELSE
                            1 /* "Draft" */
                    END AS statusId
                FROM
                    doc_status_types AS dst
                        INNER JOIN docs AS d
                            ON dst.id = d.statusId
                WHERE
                    d.id = %s
                """

        query = ' '.join(query.split())
        queryResult = self._executeQuery(query, (docId,)).fetchone()
        self._convertToDictionary(queryResult)
        return self._getResultData()
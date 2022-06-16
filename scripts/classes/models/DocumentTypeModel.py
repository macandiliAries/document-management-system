from scripts.utilities.dbConnection import DbConnection

class DocumentTypeModel(DbConnection):

    def getDocumentTypes(self):
        query = """
                SELECT
                    *
                FROM
                    doc_types
                """

        query = ' '.join(query.split())
        queryResult = self._executeQuery(query, ()).fetchall()
        self._convertToDictionary(queryResult)
        return self._getResultData()
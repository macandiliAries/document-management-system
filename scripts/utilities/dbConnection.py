from scripts.utilities.credentials import getDbCredentials
from mysql.connector import connect, Error

class DbConnection:

    __connection = None

    __cursor = None

    __affectedRows = 0

    __resultData = []

    def __init__(self):
        try:
            self.__connection = connect(**getDbCredentials())
            self.__cursor = self.__connection.cursor(prepared=True)
        except Error as error:
            print('DB Connection Error: ' + str(error))

    def _executeQuery(self, queryString: str, queryParams: tuple):
        if len(queryParams) > 0:
            self.__cursor.execute(queryString, queryParams)
        else:
            self.__cursor.execute(queryString)

        return self.__cursor

    def _commitChanges(self):
        self.__connection.commit()
        self.__affectedRows = self.__cursor.rowcount
        self.__lastRowId = self.__cursor.lastrowid

    def _convertToDictionary(self, queryResult):
        if queryResult is not None:
            temp = []
            if type(queryResult) is not list:
                temp = dict(zip(self.__cursor.column_names, queryResult))
            else:
                for row in queryResult:
                    temp.append(dict(zip(self.__cursor.column_names, row)))
            queryResult = temp

        self.__resultData = queryResult

    def _getAffectedRows(self):
        return self.__affectedRows

    def _getLastRowId(self):
        return self.__lastRowId

    def _getResultData(self):
        return self.__resultData

    def _generatePlaceHolders(self, columns):
        return '({})'.format(', '.join('?' * len(columns)))
    
    def __del__(self):
        if self.__connection is not None and self.__connection.is_connected() == True:
            self.__cursor.close()
            self.__connection.close()

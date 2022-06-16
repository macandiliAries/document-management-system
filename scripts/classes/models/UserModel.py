from scripts.utilities.dbConnection import DbConnection

class UserModel(DbConnection):

    def getUsers(self):
        query = "SELECT id, username, full_name, user_type, email, address, contact_num, status FROM users"
        queryResult = self._executeQuery(query, ()).fetchall()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def getUserBy(self, columnKey: str, columnValue: str):
        query = "SELECT * FROM users WHERE {} = %s".format(columnKey)
        queryResult = self._executeQuery(query, (columnValue,)).fetchone()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def getUserByWithIdException(self, columnKey: str, columnValue: str, id: str):
        query = "SELECT * FROM users WHERE {} = %s AND id != %s".format(columnKey)
        queryResult = self._executeQuery(query, (columnValue, id)).fetchone()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def getUserById(self, id: int):
        query = "SELECT id, username, full_name, user_type, email, address, contact_num, status FROM users WHERE id = %s"
        queryResult = self._executeQuery(query, (id,)).fetchone()
        self._convertToDictionary(queryResult)
        return self._getResultData()

    def updateUserData(self, queryParams: dict):
        setParams = ', '.join('{} = ?'.format(setKey) for setKey in queryParams['set'].keys())
        whereParams = ' AND '.join('{} = ?'.format(whereKey) for whereKey in queryParams['where'].keys())
        query = "UPDATE users SET {} WHERE {}".format(setParams, whereParams)
        queryParams = tuple(list(queryParams['set'].values()) + list(queryParams['where'].values()))
        self._executeQuery(query, queryParams)
        self._commitChanges()
        return self._getAffectedRows()

    def addNewUser(self, columns: tuple, queryParams: tuple):
        query = "INSERT INTO users (" + ', '.join(columns) + ") VALUES " + self._generatePlaceHolders(columns)
        self._executeQuery(query, queryParams)
        self._commitChanges()
        return self._getAffectedRows()

    def deleteUser(self, id: int):
        query = "DELETE FROM users WHERE id = %s"
        self._executeQuery(query, (id,))
        self._commitChanges()
        return self._getAffectedRows()
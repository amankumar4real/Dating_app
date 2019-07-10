import mysql.connector

class DBhelper:
    def __init__(self):
        try:
            self._connection=mysql.connector.connect(host="127.0.0.1", user="root", password="", database="tinderb3")
            self._cursor=self._connection.cursor()
            print("Connected to database")
        except:
            print("could not connected to database")
            exit(0)

    def search(self,key1,value1,key2,value2,table):
        self._cursor.execute("""
        SELECT * FROM `{}` WHERE `{}` LIKE '{}' AND `{}` LIKE '{}'
        """.format(table,key1,value1,key2,value2))
        data = self._cursor.fetchall()
        return data


    def searchOne(self,key1,value1,table,type):
        self._cursor.execute("""
                SELECT * FROM `{}` WHERE `{}` {} '{}'
                """.format(table, key1, type, value1))
        data = self._cursor.fetchall()
        return data


    def insert(self,insertDict,table, mode=0):
        colValue = ""
        dataValue = ""
        for i in insertDict:
            colValue = colValue + "`" + i + "`,"
            dataValue = dataValue + "'" + insertDict[i] + "',"
        if mode == 0:
            colValue = colValue + "`dp`"
            dataValue = dataValue + "'D.jpg'"
        else:
            colValue = colValue[:-1]
            dataValue = dataValue[:-1]

        query = "INSERT INTO `{0}` ({1}) VALUES ({2})".format(table, colValue, dataValue)

        try:
            self._cursor.execute(query)
            self._connection.commit()

            return 1
        except:
            return 0

    def update(self, updateDict, table, id101):
        colValue = ""
        dataValue = ""
        for i in updateDict:
            colValue = colValue + "`" + i + "`,"
            dataValue = dataValue + "'" + updateDict[i] + "',"
        colValue = colValue[:-2]
        dataValue = dataValue[:-2]
        print(colValue)
        print(dataValue)
        query = "UPDATE  `{}` SET ({})= ({}) WHERE {} = {}".format(table, colValue, dataValue, 'user_id', id101)
        try:
            self._cursor.execute(query)
            self._connection.commit()
            return 1
        except:
            return 0

    def setDp(self,filename,table1,user_id,dp,id_value):
        query = "UPDATE  `{}` SET {}= '{}'  WHERE {} ={}".format(table1, dp, filename, user_id, id_value)
        print(query)
        self._cursor.execute(query)
        self._connection.commit()




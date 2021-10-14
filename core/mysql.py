
# 
# class for open connection to mysql
# 

# libs
import mysql.connector

class Mysql_Connect:

    # constructor
    def __init__(self, host, user, password, db):

        self.host = host
        self.user = user
        self.password = password
        self.db = db     

    # Read
    def Read(self, sql_command):
        # connection
        connection = mysql.connector.connect(host = self.host, user = self.user, passwd = self.password, database = self.db)

        # io buffer cursor
        cursor = connection.cursor()

        # exec sql command
        cursor.execute(sql_command)

        # load data
        data = cursor.fetchall()

        # close connection
        connection.close()

        # return data
        return data

# CREATE DATA BASE

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE pokemon")
my_cursor.execute("SHOW DATABASES")

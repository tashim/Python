import sqlite3
from sqlite3 import Error
"""
db module
database logic
"""


def sql_connection():
    """
    function sql_connection
    creates new database connection
    :return: database connection
    """
    try:
        db = sqlite3.connect('data.db')
        return db
    except Error:
        print(Error)


def sql_create_station_status (con):
    """
    function sql_create_station_status
    creates station_status table if it does not exists
    :param con: opened database connection
    """
    sql="CREATE TABLE IF NOT EXISTS station_status("
    sql+="station_id INT,"
    sql+="last_date TEXT,"
    sql+="alarm1 INT,"
    sql+="alarm2 INT,"
    sql+="PRIMARY KEY(station_id) );"

    cursorObj = con.cursor()
    cursorObj.execute(sql)
    try:
        con.commit()  # saves all the changes we make
    except Error:
        print(Error , " - CREATE TABLE")


def sql_update_station_status(con,data):
    """
    function sql_update_station_status -updates station status data
    :param con: opened database connection
    :param data: station data
    """
    sql="insert or replace into station_status values (?, ?, ?, ?)"
    cursorObj = con.cursor()
    cursorObj.execute(sql,data)
    try:
        con.commit()  # saves all the changes we make
    except Error:
        print(Error , " - CREATE TABLE")


db=sql_connection()
sql_create_station_status(db)
db.close()
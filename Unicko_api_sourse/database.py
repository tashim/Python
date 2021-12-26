from datetime import date, datetime

from MySQLdb import ProgrammingError, IntegrityError
from Keywords import mysql_keys

import MySQLdb


class Database(object):
    def __init__(self):
        self.mydb = None

    def connect(self):
        try:
            self.mydb = MySQLdb.connect(
                host=mysql_keys["host"],
                user=mysql_keys["user"],
                password=mysql_keys["password"],
                database=mysql_keys["db_name"])
            print("Database connected.")
        except ProgrammingError:
            print("Table Not Found!")

    def create_table(self):
        mycursor = self.mydb.cursor
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS Items (
            unicko_user TEXT,
            unicko_course_ID INT,
            name TEXT,
            date INT,
            duration INT,
            recording_ID INT PRIMARY KEY NOT NULL,
            lesson TEXT
            path TEXT);""")
        mycursor.commit()

    def insert(self, unicko_user, course_id, name, date, duration, recording_id, path):
        qry = (
            "INSERT INTO video_files ("
            "unicko_user, unicko_course_ID, name, date, duration, recording_ID, path)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        mycursor = self.mydb.cursor()
        data = (unicko_user, course_id, name, date, duration, recording_id, path)
        try:
            mycursor.execute(qry, data)
            self.mydb.commit()
        except IntegrityError:
            print("Item already in DataBase!")

        # TODO: UPdate file to couse_cycle
            # TODO: 1: find all course_cycle url_unicko = course_id
        qry = ( f"SELECT code FROM coursecycle where url_conference ='{str(course_id)}'; " )
        try:
            mycursor.execute(qry)
            # TODO: 2: foreach course:
            for rec in mycursor.fetchall():
                print(rec)
                # TODO: : if exist in video_sessions course_cycle_id & video_id
                qry = ( "SELECT count(video_id) FROM video_session " +
                    f"where unicko_video_id ='{str(recording_id)}' and cycle_code='{str(rec[0])}'; " )
                print(qry)
                cursor = self.mydb.cursor()
                cursor.execute(qry)
                if cursor.fetchone()[0] <=0:
                    # TODO: : insert new entry
                    print("no")
                    qry = ( "INSERT INTO video_session "
                    "(cycle_code, video_date, video_url, unicko_video_id, unicko_meeting_id, video_duration) "
                    f"VALUES('{str(rec[0])}', '{datetime.strptime(date, '%m/%d/%y - %H:%S')}',"
                    f"'{path}', '{recording_id}', '{course_id}', '{duration}');" )
                    cursor.execute(qry)
                    self.mydb.commit()
                else:
                    print('exist')
        except IntegrityError:
            print("Error read  DataBase!")


    def recording_exists(self, recording):
        qry = "SELECT * FROM video_files WHERE recording_ID = %s"
        mycursor = self.mydb.cursor()
        data = (recording,)
        mycursor.execute(qry, data)
        if mycursor.fetchall(): return True
        else: return False

    def delete_row(self, recording):
        qry = "DELETE FROM video_files WHERE recording_ID = %s"
        mycursor = self.mydb.cursor()
        data = (recording,)
        mycursor.execute(qry, data)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")

    def get_course_ids(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT unicko_course_ID FROM video_files")
        return mycursor.fetchall()

    def get_course_recording_dates(self, course_id):
        mycursor = self.mydb.cursor()
        qry = "SELECT recording_ID, date FROM video_files WHERE unicko_course_ID = %s"
        data = (course_id[0],)
        mycursor.execute(qry, data)
        return mycursor.fetchall()

    def update_recording_lesson_number(self, lesson_number, recording_id):
        qry = "UPDATE video_files SET lesson = %s WHERE recording_ID = %s"
        mycursor = self.mydb.cursor()
        data = (lesson_number, recording_id)
        mycursor.execute(qry, data)
        self.mydb.commit()

    def insert1(self, unicko_user, course_id, name, date, duration, recording_id, path):
        mycursor = self.mydb.cursor()
        # TODO: UPdate file to couse_cycle
            # TODO: 1: find all course_cycle url_unicko = course_id
        qry = (
            f"SELECT code FROM coursecycle where url_conference ='{str(course_id)}'; "
        )
        try:
            mycursor.execute(qry)
            # TODO: 2: foreach course:
            for rec in mycursor.fetchall():
                print(rec)
                # TODO: : if exist in video_sessions course_cycle_id & video_id
                qry = (
                    "SELECT count(video_id) FROM video_session " +
                    f"where unicko_video_id ='{str(recording_id)}' and cycle_code='{str(rec[0])}'; "
                )
                print(qry)
                cursor = self.mydb.cursor()
                cursor.execute(qry)
                if cursor.fetchone()[0] <=0:
                    # TODO: : insert new entry
                    print("no")
                    qry = (
                        "INSERT INTO video_session "
                    "(cycle_code, video_date, video_url, unicko_video_id, unicko_meeting_id, video_duration) "
                    f"VALUES('{str(rec[0])}', '{datetime.strptime(date, '%m/%d/%y - %H:%S')}',"
                    f"'{path}',"
                    f"'{recording_id}', '{course_id}', '{duration}');"
                    )
                    cursor.execute(qry)
                    self.mydb.commit()
                else:
                    print('yes')
        except IntegrityError:
            print("Error read  DataBase!")



if __name__ == '__main__':
    database = Database()
    database.connect()
    #insert1(self, unicko_user, course_id, name, date, duration, recording_id, path)
    database.insert1('','823242548','name',"12/29/20 - 18:03",'duration5',"3189100",'path')

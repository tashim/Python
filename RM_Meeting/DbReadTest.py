import MySQLdb
from MySQLdb import ProgrammingError


class Database(object):
    def __init__(self):
        self.mydb = None

    def connect(self):
        if self.mydb:
            return self.mydb
        try:
            from Keywords import mysql_keys
            self.mydb = MySQLdb.connect(
                host=mysql_keys['host'],
                user=mysql_keys['user'],  # mysql_keys["user"],
                password=mysql_keys['password'],  # mysql_keys["password"],
                database=mysql_keys['database'])  # mysql_keys["db_name"])
            print("Database connected.")
        except ProgrammingError:
            print("Table Not Found!")
            exit(1)

    def run_query(self, query, data=None, commit=False):
        # # data tuple
        mycursor = self.mydb.cursor()
        try:
            if data:
                mycursor.execute(query, data)
            else:
                mycursor.execute(query)
        except:
            print("error DB")
            return None
        if commit:
            self.mydb.commit()
        return mycursor.fetchall()

    def get_cource_by_unicoID(self, uId):
        query = """SELECT url_conference,code,endDate FROM coursecycle 
            where url_conference = %s
            ; 
            """
        ret = []
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(query,(uId,))
            ret = mycursor.fetchall()
        except ProgrammingError as err:
            print('DB',err)
            exit(1)
        if len(ret)>0:
            return ret
        return None

    def get_cource_without_unicoID(self):
        query = """
        SELECT url_conference,code,endDate FROM coursecycle 
        where 
          endDate > date_add(now(), INTERVAL -33 day)  and 
          ( url_conference is null or url_conference = '' )
        ;"""
        ret = []
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(query)
            ret = mycursor.fetchall()
        except ProgrammingError as err:
            print('DB', err)
            exit(1)
        if len(ret) > 0:
            return ret
        return None

    def get_cource_with_unicoID(self):
        query = """
        SELECT url_conference,code,endDate FROM coursecycle 
        where 
            endDate > date_add(now(), INTERVAL -33 day)  
        ;"""
        ret = []
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(query)
            ret = mycursor.fetchall()
        except ProgrammingError as err:
            print('DB', err)
            exit(1)
        if len(ret) > 0:
            return ret
        return None

    def rm_unicoID_from_cource(self,cID):
        query = """
         UPDATE coursecycle SET url_conference = NULL where code = %s
        ;"""
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute(query,(cID,))
            self.mydb.commit()
        except ProgrammingError as err:
            print('DB',err)
            exit(1)

RTG_DB = Database()

RTG_DB.connect()
if __name__ == "__main__":
    ret = RTG_DB.run_query("select pathCode,pathName from path;")
    print(ret)
    print(len(ret))

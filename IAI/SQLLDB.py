import datetime
import os
import sqlite3
from tkinter import messagebox

db_name = 'IAI_test.db'
# db_name = 'test-socket.db'
df_IP = '192.168.0.132'
df_wait = 3


class DB_SQLL():
    def __init__(self):
        self.db = None
        if os.path.isfile(db_name):
            flag = False
        else:
            flag = True
        try:
            self.db = sqlite3.connect(db_name)
            self.cursor = self.db.cursor()
            self.create_def_table()
            if flag:
                self.ports_up()
        except:
            print('error connection')
            self.__del__()
            exit(1)

    def create_def_table(self):
        # print("CREATE TABLE IF NOT EXISTS   Setings")
        q = """CREATE TABLE IF NOT EXISTS   "Setings" 
        (   "id"	TEXT NOT NULL ,
            "data"	TEXT,
            PRIMARY KEY("id")   )
        ;"""
        self.cursor.execute(q)

        # q = """CREATE TABLE IF NOT EXISTS   "Device"
        q = """CREATE TABLE IF NOT EXISTS   "Device" 
        (   "Device_name"	TEXT NOT NULL,
            "Port_Tx"	INTEGER NOT NULL,
            "Port_Rx"	INTEGER NOT NULL,
            PRIMARY KEY("Device_name")  );
        """
        self.cursor.execute(q)

        # q = """CREATE TABLE IF NOT EXISTS   "Standart_test"
        q = """CREATE TABLE IF NOT EXISTS   "Standart_test" 
        (   "Type_test"	TEXT,
            "ST_Test_Name"	TEXT NOT NULL UNIQUE,
            "Device_name_Tx"	TEXT NOT NULL,
            "Device_name_Rx"	TEXT NOT NULL,
            PRIMARY KEY("ST_Test_Name") );
        """
        self.cursor.execute(q)

        # q = """CREATE TABLE IF NOT EXISTS   "Type_test"
        q = """CREATE TABLE IF NOT EXISTS   "Type_test" 
        (   "Test name"	TEXT NOT NULL UNIQUE,
            PRIMARY KEY("Test name")    );
        """
        self.cursor.execute(q)

        # q = """CREATE TABLE IF NOT EXISTS   "User_test"

        q = """CREATE TABLE IF NOT EXISTS   "User_test" 
        (   "ID_User_test"	INTEGER,
            "StTest"	TEXT,
            "Packets_count"	INTEGER,
            "Rate"	INTEGER,
            "Data"	TEXT,
            "Date"	TEXT,
            "Data_type"	INTEGER DEFAULT 0,
            "user_test_type"	TEXT,
            "cmp_ASCII"	TEXT,
            "cmp_HEX"	TEXT,
           PRIMARY KEY("ID_User_test" AUTOINCREMENT)   );
        """
        self.cursor.execute(q)

    def test_type_list(self):
        sqlite_select_query = """SELECT * from Type_test"""
        self.cursor.execute(sqlite_select_query)
        l = []
        for t in self.cursor.fetchall():
            l.append(t[0])
        return l


    def St_Test_List(self, type=None):
        if type:
            sqlite_select_query = """SELECT * from Standart_test WHERE Type_test ='%s' ;""" % type
        else:
            sqlite_select_query = """SELECT * from Standart_test ;"""
        self.cursor.execute(sqlite_select_query)
        l = []
        for t in self.cursor.fetchall():
            l.append(t)
        return l

    def tests_names_by_type(self, type=None):
        if type:
            sqlite_select_query = """SELECT ST_Test_Name from Standart_test WHERE Type_test ='%s' ;""" % type
        else:
            sqlite_select_query = """SELECT ST_Test_Name from Standart_test ;"""
        self.cursor.execute(sqlite_select_query)
        l = []
        for t in self.cursor.fetchall():
            l.append(t[0])
        return l

    def save_stand_test(self, type_test, st_test_name, device_name_tx, device_name_rx):
        sql = """insert INTO Standart_test (Type_test, ST_Test_Name, Device_name_Tx, Device_name_Rx)
        VALUES (?, ?, ?, ? )"""
        try:
            self.cursor.execute(sql, (type_test, st_test_name, device_name_tx, device_name_rx))
            self.db.commit()
        except sqlite3.DatabaseError as er:
            messagebox.showerror(title=None, message=er)
            return str(er)

    def save_new_type(self, new_type):
        sql = """insert INTO Type_test VALUES ('%s');""" % new_type
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except sqlite3.DatabaseError as er:
            messagebox.showerror(title=None, message=er)
            return str(er)

    def ports_by_dev(self, test=None):
        if test:
            sqlite_select_query = """SELECT * from Device WHERE Device_name ='%s' ;""" % test
        else:
            sqlite_select_query = """SELECT * from Device order by Device_name;"""
        self.cursor.execute(sqlite_select_query)
        dc = {}
        for dev in self.cursor.fetchall():
            dc[dev[0]] = dev[1:3]
        return dc

    def user_tests(self):
        ret = []
        sqlite_select_query = """
        SELECT * from User_test
        INNER join Standart_test on Standart_test.ST_Test_Name = User_test.StTest;"""
        self.cursor.execute(sqlite_select_query)
        for r in self.cursor.fetchall():
            dic = {}
            ret.append(dic)
            dic["st_test"] = r[1]
            dic["pac_count"] = r[2]
            dic["rate"] = r[3]
            dic["data"] = r[4]
        return ret

    def ports_list(self):
        sqlite_select_query = """SELECT * from Device"""
        self.cursor.execute(sqlite_select_query)
        return self.cursor.fetchall()

    def save_ports(self, result=None):
        if result is None:
            result = []
        sqlite_select_query1 = """
            INSERT or REPLACE INTO Device 
            (Device_name,Port_Tx, Port_Rx ) 
            VALUES(?,?,?)   ;"""
        self.cursor.executemany(sqlite_select_query1, result).fetchall()
        self.db.commit()

    def delete_test_type(self, id):
        q = f"""
        DELETE FROM User_test WHERE User_test.StTest in
(SELECT Standart_test.ST_Test_Name FROM standart_test WHERE Type_test='{id}')
        ;"""
        q2 = f"""
        DELETE FROM standart_test WHERE Type_test='{id}'
        ;"""
        q3 = f"""
        DELETE FROM Type_test WHERE `Test name`='{id}'
        ;"""
        try:
            self.cursor.execute(q)
            self.cursor.execute(q2)
            self.cursor.execute(q3)
            self.db.commit()
        except:
            self.db.rollback()

    def update_test_type(self, old, new):
        try:
            q = F"""UPDATE Type_test  SET `Test name`='{new}'  WHERE `Test name`='{old}';"""
            self.cursor.execute(q)
            q = F"""UPDATE standart_test  SET `Type_test`='{new}'  WHERE `Type_test`='{old}';"""
            self.cursor.execute(q)
            self.db.commit()
        except:
            self.db.rollback()

    def del_ports(self, key=None):
        if key is None:
            return
        sqlite_select_query1 = """
        DELETE FROM User_test
WHERE ID_User_test in
(SELECT ID_User_test FROM User_test
INNER JOIN Standart_test on Standart_test.ST_Test_Name=User_test.StTest
WHERE Standart_test.Device_name_Rx='%s' or Standart_test.Device_name_Tx='%s')
        ;""" % (key, key)
        try:
            self.cursor.execute(sqlite_select_query1).fetchall()
            # self.db.commit()
            sqlite_select_query1 = """
            DELETE FROM Standart_test WHERE Device_name_Rx = '%s' OR  Device_name_Tx = '%s' ;""" % (key, key)
            self.cursor.execute(sqlite_select_query1).fetchall()
            # self.db.commit()
            sqlite_select_query1 = """DELETE FROM Device  where Device_name = '%s'""" % key
            self.cursor.execute(sqlite_select_query1).fetchall()
            self.db.commit()
        except:
            self.db.rollback()

    def input_dev(self, dic):
        sqlite_select_query1 = """INSERT INTO Device  (Device_name,Port_Tx,Port_Rx) VALUES (?,?,?)"""
        self.cursor.execute(sqlite_select_query1, dic)
        self.db.commit()


    def save_user_test(self, utest: dict):
        data = []
        name = 'StTest, Packets_count, Rate, Data,Data_type, Date,user_test_type,cmp_ASCII,cmp_HEX'
        for key in name.replace(' ', '').split(','):
            data.append(utest[key])
        sqlite_select_query = """
        INSERT  INTO User_test(""" + name + """)VALUES(?, ?, ?, ?, ?,?,?,?,?)"""
        self.cursor.execute(sqlite_select_query, (data))
        self.db.commit()

    def update_user_test(self, utest: dict):
        data = []
        name = 'ID_User_test,StTest, Packets_count, Rate, Data,Data_type, Date,user_test_type,cmp_ASCII,cmp_HEX'
        for key in name.replace(' ', '').split(','):
            data.append(utest[key])
        sqlite_select_query = """
        INSERT or replace INTO User_test(""" + name + """)VALUES(?,?, ?, ?, ?, ?,?,?,?,?)"""
        self.cursor.execute(sqlite_select_query, (data))
        self.db.commit()

    def delete(self, ID):
        query = """DELETE FROM User_test where ID_User_test={};""".format(ID)
        self.cursor.execute(query)
        self.db.commit()

    def integration_load(self):
        sql = """
        SELECT ID_User_test,Type_test,ST_Test_Name,Device_name_Tx,Device_name_Rx,
            Date,
            Packets_count,
            Rate,
            Data
        ,(SELECT Port_Tx FROM Device WHERE Device_name = Standart_test.Device_name_Tx ) as port_Tx
        ,(SELECT Port_Rx FROM Device WHERE Device_name = Standart_test.Device_name_Rx ) as port_Rx
        , Data_type
        , user_test_type,
        cmp_ASCII,cmp_HEX,
        User_test.StTest
        FROM User_test
        INNER JOIN Standart_test on Standart_test.ST_Test_Name=User_test.StTest
    ;"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        ret = []

        for u in result:
            test = {}
            test['ID_User_test'] = u[0]
            test['Type_test'] = u[1]
            test['ST_Test_Name'] = u[2]
            test['Device_name_Tx'] = u[3]
            test['Device_name_Rx'] = u[4]
            test['Date'] = u[5]
            test['Packets_count'] = u[6]
            test['Rate'] = u[7]
            test['Data'] = u[8]
            test['port_Tx'] = u[9]
            test['port_Rx'] = u[10]
            test['Data_type'] = u[11]
            test['user_test_type'] = u[12]
            test['cmp_ASCII'] = u[13]
            test['cmp_HEX'] = u[14]
            test['StTest'] = u[15]
            ret.append(test)
        return ret

    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def get_IP(self):
        try:
            self.cursor.execute("SELECT data FROM Setings where id='IP';")
            result = self.cursor.fetchone()[0]
            return result
        except:
            self.update_IP(df_IP)
            return df_IP

    def update_IP(self, ip):
        query = """
        INSERT or REPLACE INTO Setings (id,data) VALUES('IP','%s');""" % ip
        self.cursor.execute(query)
        self.db.commit()
        result = self.cursor.fetchone()
        return result

    def get_dfWait(self):
        try:
            self.cursor.execute('SELECT data FROM Setings  where id="Wait";')
            result = self.cursor.fetchone()[0]
            return result
        except:
            self.update_dfWait(df_wait)

    def update_dfWait(self, wt):
        query = """
        INSERT or REPLACE INTO Setings (id,data) VALUES('Wait',?);"""
        self.cursor.execute(query, (wt,))
        self.db.commit()
        result = self.cursor.fetchone()
        return result

    def ports_up(self):
        update_d = []
        if os.path.isfile('port.txt'):
            with open('port.txt', 'r+') as f:
                while True:

                    text = f.readline()
                    if text == '':
                        break
                    name = text.split(':')[0]
                    pt = text.split(':')[1].split(',')[0]
                    pr = text.split(':')[1].split(',')[1].replace('\n', '')
                    update_d.append((name, pt, pr))
            self.save_ports(update_d)


DB = DB_SQLL()

if __name__ == "__main__":
    DB.ports_up()

from tkinter import messagebox

import pymysql
from pymysql import Error

# import MySQLdb  # mysql library
#
SERVER_USERNAME = "appdev"
SERVER_PASSWORD = "Tengrinews1965"
SERVER_NAME = "45.83.43.173"
DATABASE_NAME = "studentsTest2"
#
# SERVER_USERNAME = "root"
# SERVER_PASSWORD = "1234"
# SERVER_NAME = "localhost"
# DATABASE_NAME = "studentstest2"


db=None
def con_close():
    global db
    db.cursor().close()
    db.close()

def connect():
    global db
    try:
        db = pymysql.connect(SERVER_NAME, SERVER_USERNAME, SERVER_PASSWORD, DATABASE_NAME)
        return db
    except Error as e:
        messagebox.showinfo(title="error DB", message="No internet connection")
        exit(-1)

def get_curses():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM courses;')
    return cursor.fetchall()

def getLocateList():
    global  db
    name =['all']
    code = [-1]
    locate = {'name': name, 'code': code }
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Locations where idLocations%100=0;")
    for l in cursor.fetchall():
        locate['name'].append(l[1])
        locate['code'].append(l[0])
    return locate


def get_cursCycle(code):
    cursor = db.cursor()
    if code < 0:
        cursor.execute(
            """select 
                    code, courseName, updateOpendate, 
                    students.firstName, students.familyName,
                    coursecycle.courseCode                    
                from coursecycle 
                join courses on courses.courseCode=coursecycle.courseCode
                join students on students.studentID=coursecycle.teacherID
                where display=1 AND updateOpendate <= now() 
                order by updateOpendate desc;
            """)
    else:
        cursor.execute(
            """select 
                    code, courseName, updateOpendate, students.firstName, students.familyName,coursecycle.courseCode
                from coursecycle 
                join courses on courses.courseCode=coursecycle.courseCode
                join students on students.studentID=coursecycle.teacherID
                where display=1 AND updateOpendate <= now() AND
                 coursecycle.location=%s
                order by updateOpendate desc;
            """,(code,))

    name =[]
    code = []
    courseCode=[]
    courses={'name':name,'code':code,'courseCode':courseCode}
    fech = cursor.fetchall()
    # leng = len(fech)
    for i in  fech:
        if not i[4]: fname=' '
        else: fname = i[4]
        if not  i[3]: name=' '
        else: name = i[3]
        cname = i[1]
        if not i[1]: cname=' '
        else: cname = i[1]
        try:
            sdate =  ' ( '+i[2].strftime('%d-%m-%Y')+' ) '
        except:
            sdate = ' ( ' + str(i[2])+' ) '
        courses['name'].append( cname+sdate+name+' '+ fname )
        courses['code'].append(i[0] )
        courses['courseCode'].append(i[-1] )
    if courses['name'] == []:
        courses['name'].append( 'no courses')
        courses['code'].append(-1)
        courses['courseCode'].append(-1)
        db.commit()
    return courses


def get_lessons(code):
    # print(code)
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM sessionspercycle2 "
        "join session_type on session_type.TypeCode=sessionspercycle2.sessionType "
        "where cyclecode=%s order by session_num",(code,))
    return cursor.fetchall()
    pass

def getStudents(code):
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT 
           students.studentID,students.mobileNumber,
            courseCycleCode,firstName,familyName ,
            examMark,projectMark
            FROM studentspercycle
            join students on students.studentID=studentspercycle.studentID
            join coursecycle on coursecycle.code=studentspercycle.courseCycleCode
            join coursesperstudent on students.studentID=coursesperstudent.student and coursecycle.courseCode=coursesperstudent.course
            where studentspercycle.courseCycleCode=%s
            ;
        """,code)
    # db.close()
    return cursor.fetchall()

def getMark(data):
    cursor = db.cursor()
    cursor.execute(
    "SELECT projectMark,examMark FROM studentsTest2.coursesperstudent where %s=student and course=%s ;"
    ,(data[0],data[1]))
    rez = cursor.fetchone()
    db.commit()
    return  rez

def db_saveMark(edit_box):

    # print(edit_box.courseCode)
    # print(edit_box.st_ID)
    # print(edit_box.value)

    if edit_box.notTest:
        if int(edit_box.value) == edit_box.pMark :
            return 0
        # print('proj',edit_box.value)
        str ="""
            UPDATE 
                coursesperstudent 
            set projectMark =%s
            where %s=student and course=%s 
            ;"""
    else:
        if int(edit_box.value) == edit_box.eMark :
            return 0
        # print('exam',edit_box.value)
        str ="""
            UPDATE 
                coursesperstudent 
            set examMark =%s
            where %s=student and course=%s 
            ;"""
    cursor = db.cursor()
    cursor.execute(str
     ,(edit_box.value,edit_box.st_ID,edit_box.courseCode))
    rez = cursor.fetchone()
    db.commit()
    return  rez

def get_visit(code,stID,lesID):
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT 
            visit
            FROM student_visit
            where cycle=%s and studentID=%s and %s=session
            ;
        """,(code,stID,lesID))
    rez = cursor.fetchall()
    if not rez:
        cursor.execute(
            """
            INSERT INTO student_visit (cycle, studentID, session, visit) VALUES ('%s', %s, '%s', 0);
            """
            ,(code,stID,lesID)
        )
        db.commit()
        return  False

    else:
        return rez[0][0]

def db_update(code,stID,lesID,val):
    cursor = db.cursor()
    cursor.execute(
        """
            UPDATE student_visit set visit=%s
            where cycle=%s and studentID = %s and session=%s;
        """,
        (val,code,stID,lesID) )
    db.commit()
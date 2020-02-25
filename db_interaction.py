import psycopg2
import datetime

def lecturer_module_list(lecturer_id):
    try:
        conn = psycopg2.connect(
            host="attendance-manager.cstueihbr6n2.eu-west-1.rds.amazonaws.com",
            database="AttendanceManager",
            user="Developer",
            password="rainforestbuildercode"
        )

        # Create Cursor
        cur = conn.cursor()
    except psycopg2.OperationalError as e:
        return False
    else:
        cur.execute('SELECT * FROM lecturer_assignments(' + str(lecturer_id) + ')')
        results = cur.fetchall()
        module_names = dict()
        for result in results:
            module_names[result[0]] = result[1]

        return module_names

    cur.close()
    conn.close()

def insert_new_lecture(module_id, lecturer_id):
    todays_date = datetime.date.today()
    try:
        conn = psycopg2.connect(host="localhost", database="AttendanceManager", user="postgres", password="Peapot1997")
        # Create Cursor
        cur = conn.cursor()
    except psycopg2.OperationalError as e:
        return False
    else:
        cur.execute("INSERT INTO lecture (module_id, lecturer_id, date_taught) VALUES (" +
                    str(module_id) + ", " +
                    str(lecturer_id) + ", '" +
                    str(todays_date) +
                    "') RETURNING lecture_id;")
        conn.commit()
        lecture_id = cur.fetchone()[0]
        return lecture_id

    cur.close()
    conn.close()

def lecture_attendance_list(lecture_id):
    try:
        conn = psycopg2.connect(host="localhost", database="AttendanceManager", user="postgres", password="Peapot1997")
        # Create Cursor
        cur = conn.cursor()
    except psycopg2.OperationalError as e:
        return False
    else:
        cur.execute('SELECT * FROM lecture_attendance(' + str(lecture_id) + ')')
        results = cur.fetchall()
        attendance_list = []
        for result in results:
            attendance_list.append(result[2] + ' - ' + result[3])

        return attendance_list
        cur.close()
        conn.close()

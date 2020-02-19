import psycopg2
import bcrypt

def authenticate_lecturer(email, password):
    # DB Connection
    try:
        conn = psycopg2.connect(host="localhost", database="AttendanceManager", user="postgres", password="Peapot1997")
        # Create Cursor
        cur = conn.cursor()
    except psycopg2.OperationalError as e:
        return False
    else:
        # Test Conn
        cur.execute("SELECT lecturer_id, lecturer_password FROM lecturer WHERE email = '" + email + "'")
        result = cur.fetchone()

        if result is not None:
            # assign fetched result
            hashed_password = result[1]
            lecturer = result[0]
            # close database connections
            cur.close()
            conn.close()
        else:
            cur.close()
            conn.close()
            return False

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        print('lecturer id: ' + str(lecturer))
        return True
    else:
        print('INCORRECT PASSWORD')
        return False

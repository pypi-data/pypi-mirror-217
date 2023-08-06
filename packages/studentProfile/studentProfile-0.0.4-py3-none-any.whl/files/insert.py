import sqlite3
conn = sqlite3.connect("database.db")

# insert function


def insert_values():
    try:
        name = input("Enter student's name: ")
        roll_num = int(input("Enter student's roll number : "))
        stu_class = int(input("Enter student's class(numeric): "))
        contact_num = int(input("Enter student's contact number: "))
        conn.execute('''
            INSERT INTO student_profile(Name, Roll_num,
            Class, Contact_num) VALUES(?,?,?,?)
            ''', (name, roll_num, stu_class, contact_num))
        print("Done!")
        conn.commit()
        conn.close()
    except ValueError:
        print("Invalid Entry!")
    except sqlite3.OperationalError as er:
        print("there is table to enter these data!", str(er))
    except sqlite3.IntegrityError:
        print("Similar Roll Number Is Not Allowed!")

import sqlite3
conn = sqlite3.connect("database.db")

# delete entry by roll number


def delete_values():
    roll_num = int(input("Enter student roll number to be deleted: "))
    try:
        conn.execute('''
            DELETE FROM student_profile WHERE Roll_num=?
        ''', (roll_num,))
        print("Done!")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as err:
        print(err)

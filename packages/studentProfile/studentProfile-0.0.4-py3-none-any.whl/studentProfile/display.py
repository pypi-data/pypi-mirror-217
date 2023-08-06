import sqlite3
conn = sqlite3.connect("database.db")


def display_values():
    print("DISPLAY DATA THROUGH ROLL NUMBER")
    roll = int(input("Enter the roll number: "))
    try:
        cursor = conn.execute(
            "SELECT Roll_num FROM student_profile WHERE Roll_num=?", (roll,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Access the value and convert it to an integer
            roll_num = int(result[0])
        else:
            # Handle the case when no row is found
            roll_num = None
        if roll_num == None:
            print("Roll number: ", roll, " not found!")
        else:
            data = conn.execute('''
                SELECT * FROM student_profile WHERE Roll_num=?
                ''', (roll_num,))
            for n in data:
                print("Roll number: ", n[0], ",", " Name: ", n[1],
                      ","" Class: ", n[2], ","" Contact number: ", n[3],)
    except sqlite3.OperationalError as err:
        print(err)

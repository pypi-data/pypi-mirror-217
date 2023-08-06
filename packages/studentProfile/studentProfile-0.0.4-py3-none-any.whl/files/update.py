import sqlite3
conn = sqlite3.connect("database.db")

# update through roll number


def update_name():
    print("UPDATE DATA TROUGH ROLL NUMBER")
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
            name = input("Enter update name: ")
            stu_class = int(input("Enter update class: "))
            contact_num = int(input("Enter update contact number: "))

            conn.execute('''
                UPDATE student_profile SET Name=?,
                Class=?, Contact_num=? WHERE Roll_num=?
                ''', (name, stu_class, contact_num, roll_num,))
            print("Done!")
            conn.commit()
            conn.close()
    except sqlite3.OperationalError as err:
        print(err)

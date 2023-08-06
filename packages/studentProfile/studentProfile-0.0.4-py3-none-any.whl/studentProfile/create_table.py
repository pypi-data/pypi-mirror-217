import sqlite3
conn = sqlite3.connect("database.db")

# create table


def create_table():
    conn.execute('''
    CREATE TABLE IF NOT EXISTS student_profile (
    Roll_num IINTEGER PRIMARY KEY ,
    Name TEXT,
    Class INTEGER,
    Contact_num INTEGER
    )
    ''')
    conn.commit()
    conn.close()
    print('''You have created student profile table with entries Roll number,
Name, Class(in numeric) and contact number.''')

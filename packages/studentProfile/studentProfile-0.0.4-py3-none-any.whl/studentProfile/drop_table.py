import sqlite3
conn = sqlite3.connect("database.db")

# fucntion to drop a table


def drop_table():
    try:
        table_name = input("Enter a table name to drop: ")
        conn.execute('''
            DROP TABLE {}
            '''.format(table_name))
        print("You have dropped table ", table_name)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as err:
        print(err)

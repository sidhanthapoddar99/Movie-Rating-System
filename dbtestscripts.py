import sqlite3

with sqlite3.connect('softwareproject.db') as con:
        cur =con.cursor()
        cur.execute('''SELECT* FROM User_Auth''')
        rows = cur.fetchall()
print(rows)

import sqlite3
con = sqlite3.connect("data.db")
c = con.cursor()

for i in range(1, 29):
    c.execute("INSERT INTO sem2 VALUES (?, ?, ?, ?, ?, ?, ?)", 
        (
            i,
            00.00,
            00.00,
            00.00,
            00.00,
            00.00,
            00.00
        )
        )
    con.commit()

con.close()
import sqlite3 as sq

with sq.connect("saper.db") as con:
    cur = con.cursor()
    # delete every time for rewriting to conveniently run script
    cur.execute("DROP TABLE IF EXISTS users")

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sex INTEGER NOT NULL DEFAULT 1,
        old INTEGER,
        score INTEGER
    )""")

    sql = "INSERT INTO users (name, old, score) VALUES('Алексей', 18, 1000)"
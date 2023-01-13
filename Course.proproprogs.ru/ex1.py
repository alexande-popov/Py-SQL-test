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

    ## Fill the table
    row1_sql = "INSERT INTO users VALUES(1, 'Михаил', 1, 19, 1000)"
    cur.execute(row1_sql)

    cur.execute("INSERT INTO users (name, sex, old, score) VALUES('Александр', 1, 18, 500)")
    cur.execute("INSERT INTO users (name, old, score) VALUES('Алексей', 22, 200)")  # sex is DEFAULT
    cur.execute("INSERT INTO users (name, sex, old, score) VALUES('Мария', 2, 30, 1200)")

    rows56_sql = """
        INSERT INTO users (name, old, score) VALUES
            ('Александр', 12, 100),
            ('Григорий', 57, 1500)
    """
    cur.execute(rows56_sql)

    # 17 is not in order for increment, but ok.
    # if 1, 2 or so on -- IntegrityError: UNIQUE constraint failed: users.user_id
    row7_sql = "INSERT INTO users VALUES(17, 'Николай', 1, 35, 900)"
    cur.execute(row7_sql)

    # typing: old INTEGER = 'twenty'
    cur.execute("INSERT INTO users (name, sex, old, score) VALUES('Ольга', 2, 'twenty', 1200)")

    ## Select
    select_sql = "SELECT * FROM users WHERE score >= 500 AND sex = 1 ORDER BY score ASC LIMIT 2, 3"
    cur.execute(select_sql)

    for result in cur:
        print(result)

    # result as list of tuples
    result = cur.fetchall()
    # print(result)

    # # in order by one
    # print(cur.fetchone(), '\n', cur.fetchone())



import sqlite3 as sq

with sq.connect("my_db.db") as con:
    cur = con.cursor()
    # delete every time for rewriting to conveniently run script
    cur.execute("DROP TABLE IF EXISTS tab1")
    cur.execute("DROP TABLE IF EXISTS tab2")

    # create tables
    cur.execute("""CREATE TABLE IF NOT EXISTS tab1 (
        score INTEGER NOT NULL DEFAULT 0,
        `from` TEXT NOT NULL DEFAULT 'tab1'
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS tab2 (
        val INTEGER NOT NULL DEFAULT 0,
        type TEXT NOT NULL DEFAULT 'tab2'
    )""")

    cur.execute("INSERT INTO tab1 (score) VALUES (100), (200), (300)")
    cur.execute("INSERT INTO tab2 (val)   VALUES (200), (300), (400)")

    cur.execute("SELECT * FROM tab1")
    print("tab1:")
    for result in cur: print(result)
    cur.execute("SELECT * FROM tab2")
    print("tab2:")
    for result in cur: print(result)
    print()


    # UNION
    cur.execute("""
    SELECT score, `from` FROM tab1
    UNION SELECT val, type FROM tab2
    """)
    print("Merge all by rows:")
    for result in cur: print(result)

    cur.execute("""
        SELECT score FROM tab1
        UNION SELECT val FROM tab2
        """)
    print("Merge with unique scores:")
    for result in cur: print(result)

    cur.execute("""
    SELECT score, 'table 1' as tbl FROM tab1 WHERE score IN(300, 400)
    UNION SELECT val, 'table 2' FROM tab2
    ORDER BY score DESC
    LIMIT 3
    """)
    print("Merge with conditions and sorting")
    for result in cur: print(result)

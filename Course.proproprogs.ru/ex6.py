import sqlite3 as sq

with sq.connect("saper.db") as con:
    cur = con.cursor()

    cur.execute("SELECT * FROM users")
    print("Table users:")
    for result in cur: print(result)

    cur.execute("SELECT * FROM games")
    print("Table games:")
    for result in cur: print(result)
    print()


    cur.execute("SELECT name, sex, games.score FROM users, games LIMIT 16")
    print("Merge tables: each games.score juxtaposes users.name & users.sex")
    for result in cur: print(result)

    cur.execute("""
        SELECT name, sex, games.score FROM games
        JOIN users ON games.user_id = users.rowid
        """)
    print("Join table: users.name, users.sex, games.score")
    for result in cur: print(result)

    # Delete user from table 'users' to show the work of INNER JOIN and LEFT JOIN
    delete_sql = "DELETE FROM users WHERE user_id = 3"
    cur.execute(delete_sql)
    print(delete_sql)

    cur.execute("""
        SELECT name, sex, games.score FROM games
        INNER JOIN users ON games.user_id = users.rowid
        """)
    print("INNER JOIN table: users.name, users.sex, games.score")
    for result in cur: print(result)

    cur.execute("""
           SELECT name, sex, games.score FROM games
           LEFT JOIN users ON games.user_id = users.rowid
           """)
    print("LEFT JOIN table: users.name, users.sex, games.score")
    for result in cur: print(result)

    # restore table user
    cur.execute("INSERT INTO users VALUES (3, 'Алексей', 1, 22, 200)")

    cur.execute("""
        SELECT name, max(games.score) as best FROM games
        JOIN users ON games.user_id = users.rowid
        GROUP BY name
        ORDER BY best DESC
        """)
    print("Top: ordered best result for users")
    for result in cur: print(result)


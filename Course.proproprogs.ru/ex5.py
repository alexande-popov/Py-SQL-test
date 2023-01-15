import sqlite3 as sq

with sq.connect("saper.db") as con:
    cur = con.cursor()
    # delete every time for rewriting to conveniently run script
    cur.execute("DROP TABLE IF EXISTS games")

    cur.execute("""CREATE TABLE IF NOT EXISTS games (
        user_id INTEGER,
        score INTEGER,
        time INTEGER
    )""")


    ## Fill the table
    insert_query = """
    INSERT INTO games VALUES
        (1, 200, 100000),
        (1, 300, 110010),
        (2, 500, 100010),
        (1, 400, 201034),
        (3, 100, 200010),
        (2, 600, 210000),
        (2, 300, 210010)
    """
    cur.execute(insert_query)
    print('Create table', insert_query)


    ## aggregating functions
    cur.execute("SELECT user_id, count() FROM games WHERE user_id=1")
    print('Count all games of user 1')
    for result in cur: print(result)

    cur.execute("SELECT count(DISTINCT user_id) as uniq_users FROM games")
    print('The number of unique users')
    for result in cur: print(result)

    cur.execute("SELECT user_id, sum(score) as scores FROM games WHERE user_id=1")
    print('The sum of scores for user 1')
    for result in cur: print(result)

    ## group by
    cur.execute("""
    SELECT user_id, sum(score) as sum
    FROM games 
    GROUP BY user_id
    """)
    print('The sum of scores for all users, ordered')
    for result in cur: print(result)

    cur.execute("""
    SELECT user_id, sum(score) as sum
    FROM games 
    WHERE score > 300
    GROUP BY user_id
    ORDER BY sum DESC
    LIMIT 2
        """)
    print('The sum of scores for all users, ordered and with conditions')
    for result in cur: print(result)




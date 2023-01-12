# example from  https://thecode.media/sqlite-py/

import sqlite3

# open file
con = sqlite3.connect('my_sqlite.db')

# --- CREATE TABLE a ---
# open database
with con:
    # take table with such name, Cursor object
    data = con.execute("SELECT COUNT(*) FROM SQLITE_MASTER WHERE type='table' AND name='a'")

    for d in data:
        # if no such table
        if d[0] == 0:
            # create db
            with con:
                sql = '''
                    CREATE TABLE a (
                        id INTEGER PRIMARY KEY,
                        colu1 INTEGER,
                        colu2 VARCHAR(20)
                    );
                '''
                print(sql)
                con.execute(sql)

            # add data
            sql = 'INSERT INTO a (id, colu1, colu2) VALUES(?, ?, ?)'
            data = [
                (1, 11, '21'),
                (2, 12, '22'),
                (3, 17, '27')
            ]
            with con:
                con.executemany(sql, data)

# --- CREATE TABLE b ---
# open database
with con:
    # take table with such name, Cursor object
    data = con.execute("SELECT COUNT(*) FROM SQLITE_MASTER WHERE type='table' AND name='b'")

    for d in data:
        # if no such table
        if d[0] == 0:
            # create db
            with con:
                sql = '''
                    CREATE TABLE b (
                        coluA VARCHAR(20),
                        coluB VARCHAR(20),
                        id INTEGER PRIMARY KEY
                    );
                '''
                print(sql)
                con.execute(sql)

            # add data
            sql = 'INSERT INTO b (coluA, coluB) VALUES(?, ?)'
            data = [
                ('aA', 'aB'),
                ('bA', 'bB')
            ]
            with con:
                con.executemany(sql, data)

# --- CREATE TABLE ab BASED ON a AND b ---
# open database
with con:
    # take table with such name, Cursor object
    data = con.execute("SELECT COUNT(*) FROM SQLITE_MASTER WHERE type='table' AND name='ab'")

    for d in data:
        # if no such table
        if d[0] == 0:
            # create db
            with con:
                sql = '''
                    CREATE TABLE ab (
                        ab_id INTEGER PRIMARY KEY,
                        ab_colu1 VARCHAR(20),
                        ab_colu2 VARCHAR(20),
                        ab_colu3 VARCHAR,
                        FOREIGN KEY (ab_colu1) REFERENCES a(colu2),
                        FOREIGN KEY (ab_colu2) REFERENCES b(coluA)
                    );
                '''
                print(sql)
                con.execute(sql)

            # add data
            sql = 'INSERT INTO ab (ab_colu1, ab_colu2, ab_colu3) VALUES(?, ?, ?)'
            data = [
                ('27', 'aB', 'something')
            ]
            with con:
                con.executemany(sql, data)

# print table to screen
with con:
    data_a  = con.execute('SELECT * FROM a')
    data_b  = con.execute('SELECT * FROM b')
    data_ab = con.execute('SELECT * FROM ab')

    for i in [data_a, data_b, data_ab]:
        print('\n')
        for d in i:
            print(d)

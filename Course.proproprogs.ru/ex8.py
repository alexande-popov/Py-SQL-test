import sqlite3 as sq

with sq.connect("students.db") as con:
    cur = con.cursor()
    # delete every time for rewriting to conveniently run script
    cur.execute("DROP TABLE IF EXISTS students")
    cur.execute("DROP TABLE IF EXISTS marks")
    cur.execute("DROP TABLE IF EXISTS females")

    # create tables
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER  PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sex INTEGER  NOT NULL DEFAULT 1,
        old INTEGER NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS marks (
        id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        mark INTEGER NO NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS females (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            sex INTEGER  NOT NULL DEFAULT 1,
            old INTEGER NOT NULL
        )""")

    students = [
        ('Коля', 1, 17),
        ('Маша', 2, 18),
        ('Вася', 1, 19),
        ('Даша', 2, 17)
    ]
    marks = [
        (1, 'Си', 4),
        (1, 'Физика', 3),
        (1, 'Вышка', 5),
        (1, 'Физра', 5),
        (2, 'Си', 3),
        (2, 'Вышка', 4),
        (2, 'Химия', 3),
        (3, 'Си', 4),
        (3, 'Черчение', 3),
        (3, 'Физика', 5)
    ]
    con.executemany("INSERT INTO students (name, sex, old) VALUES (?, ?, ?)", students)
    cur.executemany("INSERT INTO marks (id, subject, mark) VALUES (?, ?, ?)", marks)

    cur.execute("SELECT * FROM students")
    print("Students:")
    for result in cur: print(result)
    cur.execute("SELECT * FROM marks")
    print("Marks:")
    for result in cur: print(result)
    print()


    # Из таблицы students выбрать id Маши,
    # а из таблицы marks выбрать тех, у кого оценка по Си выше, чем у Маши
    Masha_id_sql = "SELECT id FROM students WHERE name='Маша'"
    Masha_id = cur.execute("SELECT id FROM students WHERE name='Маша'")
    print("id Маши", Masha_id.fetchall())

    Masha_C_mark_sql = f"SELECT mark FROM marks WHERE id=({Masha_id_sql}) AND subject LIKE 'Си'"
    Masha_C_mark = cur.execute(Masha_C_mark_sql)
    print("Оценка Маши по Си", Masha_C_mark.fetchall())

    res = cur.execute(f"SELECT id FROM marks WHERE subject LIKE 'Си' AND mark > ({Masha_C_mark_sql})")
    print("Список тех, кто сильнее Маши по СИ", res.fetchall())

    result_sql = f"""
    SELECT marks.id, name, subject, mark FROM marks 
    JOIN students ON marks.id = students.id
    WHERE subject LIKE 'Си' AND mark > ({Masha_C_mark_sql})
    """
    res = cur.execute(result_sql)
    print("Список тех, кто сильнее Маши по СИ", res.fetchall())


    # Вставим в таблицу females всех девочек из таблицы students
    insert_sql = "INSERT INTO females SELECT * FROM students WHERE sex = 2"
    cur.execute(insert_sql)
    cur.execute("SELECT * FROM females")
    print("\nВставили девочек в females")
    for result in cur: print(result)


    # вложенные запросы в UPDATE
    update_sql = """UPDATE marks SET mark = 0 WHERE mark <= (SELECT min(mark) FROM marks WHERE id = 1)"""
    cur.execute(update_sql)
    cur.execute("SELECT * FROM marks")
    print("\nОбнулим те оценки, которые не лучше, чем худшая у оценка у id = 1")
    for result in cur: print(result)


    # вложенные запросы в DELETE
    delete_sql = """DELETE FROM students WHERE old < (SELECT old FROM students WHERE id = 2)"""
    cur.execute(delete_sql)
    cur.execute("SELECT * FROM students")
    print("\nУдалим студентов, которые младше Маши")
    for result in cur: print(result)
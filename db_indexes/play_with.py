import sqlite3 as sq
import random


def do_insert_template(table_name, **kwargs):
    """Return string 'INSERT INTO table_name ({field1, ...) VALUES (val1, ...);'"""

    keys = [str(k) for k in kwargs.keys()]
    vals = [f"'{v}'" if isinstance(v, str)  else str(v) for v in kwargs.values()]

    fields_names = ", ".join(keys)
    values = ", ".join(vals)

    sql_insert_val_args = f"INSERT INTO {table_name} ({fields_names}) VALUES ({values})"

    return sql_insert_val_args


db_name = "my_db"
with sq.connect(f"{db_name}.db") as con:
    cur = con.cursor()

    table_name = "t"
    target_field = "col1"
    index_name = target_field + "_inx"

    # delete every time for rewriting to conveniently run script
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"DROP INDEX IF EXISTS {index_name}")

    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
        {target_field} INTEGER,
        col2 INTEGER
    )""")
    cur.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({target_field})")

    ## Fill the table
    cardinality = 100
    for i in range(cardinality):

        val1 = random.randint(0, 1000)
        val2 = random.randint(0, 1000)

        insert_sql = do_insert_template(table_name=table_name, col1=val1, col2=val2)
        cur.execute(insert_sql)

        cur.execute(f"SELECT * FROM {table_name}")

        # for result in cur:
        #     print(result)
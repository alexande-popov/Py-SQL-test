import sqlite3 as sq
import random
import time

def measure_execution_time(fn):
    def wrapper(*args, **kwargs):
        timestart = time.time()
        fn(*args, **kwargs)
        delta = time.time() - timestart
        print(f"Execution time: {delta} s.")
    return wrapper


def do_insert_template(name, **kwargs):
    """Return string 'INSERT INTO table_name ({field1, ...) VALUES (val1, ...);'"""

    keys = [str(k) for k in kwargs.keys()]
    vals = [f"'{v}'" if isinstance(v, str)  else str(v) for v in kwargs.values()]

    fields_names = ", ".join(keys)
    values = ", ".join(vals)

    sql_insert_val_args = f"INSERT INTO {name} ({fields_names}) VALUES ({values});"

    if False:
        print(sql_insert_val_args)

    return sql_insert_val_args


def create_table(cursor, name, **kwargs):
    """Create table with name `name` and fields from kwargs.

    :Example: create_table(1, "t", col1="INTEGER", col2="INTEGER")"""

    field_type = ",\n\t".join([f"{k} {v}" for k, v in kwargs.items()])

    drop_table_sql = f"DROP TABLE IF EXISTS {name};"
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {name} (\n\t{field_type}\n);"

    print(drop_table_sql)
    print(create_table_sql)

    cursor.execute(drop_table_sql)
    cursor.execute(create_table_sql)


def drop_index(cursor, index_name):
    drop_index_sql = f"DROP INDEX IF EXISTS {index_name};"
    print(drop_index_sql)
    cursor.execute(drop_index_sql)

def create_index(cursor, index_name, table_name, *args, drop_previos=False):
    """Create index with name `index_name` on table `table_name` on columns *args

    :Example: create_index(cursor, "inx_name", "table_name", *("col1", "col2"))"""

    target_columns = ", ".join([a for a in args])

    create_index_sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({target_columns});"
    print(create_index_sql)

    if drop_previos:
        drop_index(cursor, index_name)
    cursor.execute(create_index_sql)


def random_fill(cursor, table, cardinality=10):
    """Random fill the table"""

    for i in range(cardinality):

        # val1 = random.randint(0, 1000)
        # val2 = random.randint(0, 1000)
        # insert_sql = do_insert_template(name=table["name"], col1=val1, col2=val2)

        field_val = {}
        for k in table["fields"]:
            field_val[k] = random.randint(0, 1000)

        insert_sql = do_insert_template(name=table["name"], **field_val)

        cursor.execute(insert_sql)


db_name = "my_db"
with sq.connect(f"{db_name}.db") as con:
    cur = con.cursor()

    # Define table properties
    tbl_prop = {"name": "t",
                "fields": ("col1", "col2"),
                "types": ("INEGER", "INTEGER")}

    # Define index properties
    target_field = ("col1",)
    index_name = "_".join(target_field) + "_inx"


    is_exist_sql = f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{tbl_prop['name']}'"
    is_created = len(cur.execute(is_exist_sql).fetchall()) == 1
    # is_created = False
    if not is_created:
        create_table(cursor=cur, name=tbl_prop["name"], col1="INTEGER", col2="INTEGER")
        #create_index(cur, index_name, tbl_prop["name"], *target_field)
        random_fill(cur, tbl_prop, 10_000)

    @ measure_execution_time
    def select():
        for i in range(5_000):
            cur.execute(f"SELECT * FROM {tbl_prop['name']} WHERE col1 > 995 AND col1 < 1000 ORDER BY col1")


    # without index
    create_table(cursor=cur, name=tbl_prop["name"], col1="INTEGER", col2="INTEGER")
    drop_index(cur, index_name)
    random_fill(cur, tbl_prop, 10_000)
    select()

    # with index
    create_table(cursor=cur, name=tbl_prop["name"], col1="INTEGER", col2="INTEGER")
    create_index(cur, index_name, tbl_prop["name"], *target_field)
    random_fill(cur, tbl_prop, 10_000)
    select()


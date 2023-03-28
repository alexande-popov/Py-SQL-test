import sqlite3 as sq
import random


def do_template(table_name, **kwargs):
    """Return string 'INSERT INTO table_name ({field1, ...) VALUES (val1, ...);'"""

    keys = [str(k) for k in kwargs.keys()]
    vals = [f"'{v}'" if isinstance(v, str)  else str(v) for v in kwargs.values()]

    fields_names = ", ".join(keys)
    values = ", ".join(vals)

    sql_insert_val_args = f"INSERT INTO {table_name} ({fields_names}) VALUES ({values});"

    return sql_insert_val_args


s = do_template(table_name="t", a=1, b='2')
print(s)
for i in range(10):
    val1 = random.randint(0, 1000)
    val2 = random.randint(0, 1000)
    s = do_template(table_name="t", Col1=val1, Col2=val2)
    print(s)

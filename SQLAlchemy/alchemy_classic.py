# pip install mysql-connector-python
# pip install sqlalchemy

from sqlalchemy import create_engine, select, Table, Column, Integer,   String, MetaData, ForeignKey

# Метаданные-это информация о данных в БД; например, информация о таблицах и столбцах, в которых мы храним данные.
meta = MetaData()

# создаём таблицы
# создаём таблицы
authors = Table('Authors', meta,
     Column('id_author', Integer, primary_key=True),
     Column('name', String(250), nullable = False)
)

books = Table('Books', meta,
     Column('id_book', Integer, primary_key=True),
     Column('title', String(250), nullable = False),
     Column('author_id', Integer, ForeignKey("Authors.id_author")),
     Column('genre', String(250)),
     Column('price', Integer)
)

print('--- Таблица Authors ---')
print(books.c.author_id)
print(books.columns.author_id)  # the same
print(books.primary_key)

print('\n--- Таблица Books ---')
print(authors.c.name) # print(books.columns.author)
print(authors.primary_key)
print(authors.c)

# подключаемся к бд и заносим данные
# субд+драйвер://юзер:пароль@хост:порт/база
engine = create_engine('sqlite:///alchemy.db', echo=True)

print('\n--- Create tables ---')
meta.create_all(engine) # или books.create(engine), authors.create(engine)

conn = engine.connect()

print('\n--- Fill the table Authors ---')
ins_author_query = authors.insert().values(name = 'Lutz')
conn.execute(ins_author_query)

print('\n--- Fill the table Books ---')
ins_book_query = books.insert().values(title = 'Learn Python', author_id = 1, genre = 'Education', price = 1299)
conn.execute(ins_book_query)
ins_book_query2 = books.insert().values(title = 'Clear Python', author_id = 1, genre = 'Education', price =956)
conn.execute(ins_book_query2)

print('\n--- Select from the table Books ---')
books_gr_1000_query = books.select().where(books.c.price > 1000) # SELECT * FROM Books WHERE Books.price > 1000;
result = conn.execute(books_gr_1000_query)

for row in result:
   print (row)

# print('\n--- Select from the tables Books and Authors ---')
# s = select([books, authors]).where(books.c.author_id == authors.c.id_author)
# result = conn.execute(s)
#
# for row in result:
#    print (row)

conn.commit()
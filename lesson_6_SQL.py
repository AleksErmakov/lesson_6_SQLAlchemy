import sqlalchemy
import json
from models import Base, Shop, Publisher, Stock, Sale, Book
from sqlalchemy.orm import sessionmaker

DATA_BASE = 'postgresql'
LOGIN = 'postgres'
PASSWORD = '-----'
HOST = '5432'
NAME_DB = 'lesson_6'

DSN = f'{DATA_BASE}://{LOGIN}:{PASSWORD}@localhost:{HOST}/{NAME_DB}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables(engine):
    Base.metadata.create_all(engine)


def insert_tables(file_name):
    with open(f'{file_name}', 'r') as fp:
        data = json.load(fp)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]

        session.add(model(id=record.get('pk'), **record.get('fields')))


if __name__ == '__main__':
    create_tables(engine)
    insert_tables('test_base.json')

session.commit()

if __name__ == '__main__':

    path_search = str(input('Выберете вариант поиска: "name" или "id" издателя: '))

    if path_search == 'name':
        name_publisher = str(input("Введите имя издателя: "))
        sel = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name.like(name_publisher))
        print('Книги издателя продаются в магазине (id. Name): ')
        for el in sel:
            print(el)

    else:
        id_publisher = int(input("Введите id издателя: "))
        sel = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == id_publisher)
        print('Книги издателя продаются в магазине (id. Name): ')
        for el in sel:
            print(el)


session.close()


from data import db_session
from data.halls import Hall
from data.items import Item
from data.shelf import Shelf


def add():
    db_session.global_init('db/base.db')
    session = db_session.create_session()

    # name, top, left, width, height
    halls = [['name', 1, 2, 3, 4], ['name1', 11, 22, 33, 44]]
    # type, halls_id, top, left, width, height
    items = [['logo.png', 1, 50, 100, 200, 200], ['logo.png1', 2, 11, 22, 33, 44]]

    for i in halls:
        hall = Hall()
        hall.name = i[0]
        hall.top = i[1]
        hall.left = i[2]
        hall.width = i[3]
        hall.height = i[4]
        session.add(hall)

    for i in items:
        item = Item()
        item.type = i[0]
        item.halls_id = i[1]
        item.top = i[2]
        item.left = i[3]
        item.width = i[4]
        item.height = i[5]
        session.add(item)

    session.commit()


def add_1():
    db_session.global_init('db/base.db')
    session = db_session.create_session()

    # name, photo, text
    shelfs = [['11', 'logo.png', '123'], ['22', 'logo.png', '1234'], ['33', 'logo.png', '12345']]

    for i in shelfs:
        shelf = Shelf()
        shelf.name = i[0]
        shelf.photo = i[1]
        shelf.text = i[2]
        session.add(shelf)

    session.commit()
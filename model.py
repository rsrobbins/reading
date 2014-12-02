import web, datetime

db = web.database(dbn='mysql', db='reading', user='reader', pw='debug', host='127.0.0.1', port=3306)

def get_books(offset, perpage):
    return db.select('books', order='booknum ASC', offset=offset, limit=perpage)

def get_book(id):
    try:
        return db.select('books', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_book(booknum, title, author):
    db.insert('books', booknum=booknum, title=title, author=author)

def del_book(id):
    db.delete('books', where="id=$id", vars=locals())

def update_book(id, booknum, title, author):
    db.update('books', where="id=$id", vars=locals(),
        booknum=booknum, title=title, author=author)
        
def get_books_count():
		result = db.query("SELECT COUNT(*) AS total_books FROM books")[0] 
		return result		
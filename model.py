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
		
def search_titles(title, offset, perpage):
    return db.select('books', where='title LIKE $title', vars=locals(), order='booknum ASC', offset=offset, limit=perpage)		
    
def get_search_titles_count(title):
		result = db.query("SELECT COUNT(*) AS total_books FROM books WHERE title LIKE $title", vars=locals())[0] 
		return result  
		
def search_authors(author, offset, perpage):
    return db.select('books', where='author LIKE $author', vars=locals(), order='booknum ASC', offset=offset, limit=perpage)		
    
def get_search_authors_count(author):
		result = db.query("SELECT COUNT(*) AS total_books FROM books WHERE author LIKE $author", vars=locals())[0] 
		return result  		  
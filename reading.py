""" Basic web application using webpy 0.3 """
import web
import model
import os
import time
import datetime
import requests
import json
import MySQLdb

### Url mappings

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    '/(js|css)/(.*)', 'static', 
    '/images/(.*)', 'images', #this is where the image folder is located....
    '/searchtitles', 'SearchTitles',
    '/searchauthors', 'SearchAuthors',
    '/import', 'ImportBooks',        
)

### Templates
t_globals = {
    'datestr': web.datestr,
    'now': datetime.date.today(),
    'model': model,
    'pages': 0,
    'current_page': 0,
    'first_page': 0,
    'last_page': 0
}
render = web.template.render('templates', base='base', globals=t_globals)


class Index:

    def GET(self):
        """ Show page """
        params = web.input()
        page = params.page if hasattr(params, 'page') else 1
        perpage = 10
        offset = (int(page) - 1) * perpage
        bookcount = model.get_books_count()
        print "Book Count =", bookcount.total_books
        pages = bookcount.total_books / perpage
        if bookcount.total_books % perpage > 0:
            pages += 1
        t_globals["pages"] = pages
        t_globals["current_page"] = page
        if not hasattr(params, 'page'):
            t_globals["first_page"] = 0
            t_globals["last_page"] = 11
        print "page =", page
        if int(page) == t_globals["last_page"]:
            t_globals["first_page"] = t_globals["first_page"] + 10
            t_globals["last_page"] = t_globals["last_page"] + 10 
        if int(page) == t_globals["first_page"]:
            t_globals["first_page"] = t_globals["first_page"] - 10
            t_globals["last_page"] = t_globals["last_page"] - 10                    
        print "Pages =", pages
        print "first_page =", t_globals["first_page"]
        books = model.get_books(offset, perpage)
        return render.index(books)


class View:

    def GET(self, id):
        """ View single book """
        book = model.get_book(int(id))
        return render.view(book)


class New:

    form = web.form.Form(
        web.form.Textbox('booknum', web.form.notnull, 
            size=3,
            description="Book number:"),    
        web.form.Textbox('title', web.form.notnull, 
            size=100,
            description="Book title:"),
        web.form.Textbox('author', web.form.notnull, 
            size=100,
            description="Book author:"),
        web.form.Button('Book entry'),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_book(form.d.booknum, form.d.title, form.d.author)
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        model.del_book(int(id))
        raise web.seeother('/')


class Edit:

    form = web.form.Form(
        web.form.Textbox('booknum', web.form.notnull, 
            size=3,
            description="Book number:"),    
        web.form.Textbox('title', web.form.notnull, 
            size=100,
            description="Book title:"),
        web.form.Textbox('author', web.form.notnull, 
            size=100,
            description="Book author:"),
        web.form.Button('Update book entry'),
    )

    def GET(self, id):
        book = model.get_book(int(id))
        form = self.form()
        form.fill(book)
        return render.edit(book, form)


    def POST(self, id):
        form = self.form()
        book = model.get_book(int(id))
        if not form.validates():
            return render.edit(book, form)
        model.update_book(int(id), form.d.booknum, form.d.title, form.d.author)
        raise web.seeother('/')

class static:
    def GET(self, media, file):
        
        try:
            f = open(media+'/'+file, 'r')
            return f.read()
        except:
            return '' # you can send an 404 error here if you want
        
class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"            }

        if name in os.listdir('images'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('images/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()   
            
class SearchTitles:    
	
    form = web.form.Form(  
        web.form.Textbox('title', web.form.notnull, 
            size=100,
            description="Book title:"),
        web.form.Button('Search Books'),
    )	     
    
    def GET(self):
        form = self.form()
        return render.searchtitles(form)
        
    def POST(self):
        params = web.input()
        page = params.page if hasattr(params, 'page') else 1
        title = "%" + params.title.strip() + "%"        
        perpage = 10
        offset = (int(page) - 1) * perpage
        bookcount = model.get_search_titles_count(title)
        print "Book Count =", bookcount.total_books
        pages = bookcount.total_books / perpage
        t_globals["pages"] = pages
        print "Pages =", pages
        books = model.search_titles(title, offset, perpage)
        return render.searchresults(books) 
        
class SearchAuthors:    
	
    form = web.form.Form(  
        web.form.Textbox('author', web.form.notnull, 
            size=100,
            description="Book author:"),
        web.form.Button('Search Books'),
    )	     
    
    def GET(self):
        form = self.form()
        return render.searchauthors(form)
        
    def POST(self):
        params = web.input()
        page = params.page if hasattr(params, 'page') else 1
        author = "%" + params.author.strip() + "%"        
        perpage = 10
        offset = (int(page) - 1) * perpage
        bookcount = model.get_search_authors_count(author)
        print "Book Count =", bookcount.total_books
        pages = bookcount.total_books / perpage
        t_globals["pages"] = pages
        print "Pages =", pages
        books = model.search_authors(author, offset, perpage)
        return render.searchresults(books)  
        
class ImportBooks: 
    def GET(self): 
        r = requests.get('http://www.williamsportwebdeveloper.com/BookServices.php') 
        print r.status_code   
        print r.headers['content-type']   
        print r.encoding   
        # books will be a list of dictionary objects   
        books = json.loads(r.text) 
        print len(books), "books in database"
        
        # Not doing this in the model because I need to set character sets
        db = MySQLdb.connect(host="127.0.0.1", user="reader", passwd="debug", db="reading")
        db.set_character_set('utf8') 
        cur = db.cursor()
        cur.execute('SET CHARACTER SET utf8;')   
        cur.execute('SET character_set_connection=utf8;')
				
        bookcount = model.get_books_count()
        recordcount = 1
        print "bookcount", bookcount.total_books
        for book in books:   
             if recordcount > bookcount.total_books: 
                  cur.execute("INSERT INTO books (`booknum`, `title`, `author`) VALUES (%s,%s,%s)", (book["BookNum"], book["Title"], book["Author"]))    
                  print cur._executed
             recordcount = recordcount + 1  
        db.commit()   
        db.close()      
        raise web.seeother('/')                       

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
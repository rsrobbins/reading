""" Basic web application using webpy 0.3 """
import web
import model
import os
import time
import datetime

### Url mappings

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    '/(js|css)/(.*)', 'static', 
    '/images/(.*)', 'images' #this is where the image folder is located....
)

### Templates
t_globals = {
    'datestr': web.datestr,
    'now': datetime.date.today(),
    'model': model
}
render = web.template.render('templates', base='base', globals=t_globals)


class Index:

    def GET(self):
        """ Show page """
        books = model.get_books()
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

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
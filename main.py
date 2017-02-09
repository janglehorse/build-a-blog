import os
import webapp2
import jinja2


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Entry(db.Model):
    title = db.StringProperty(required=True)
    entry = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(Handler):

    def get_posts(self, limit, offset):
        # TODO: query the database for posts, and return them
        e = db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC "
                        "LIMIT {limit} OFFSET {offset}".format(limit=limit, offset=offset))
        return e

    def get(self):

        page = self.request.get("page")
        pagesize = 5

        if not page or int(page) <=1:
            page = 1
            offset = 0
        else:
            page = int(page)
            offset = int(page) * (pagesize)

        e = self.get_posts(pagesize, offset)

        self.render('main.html', entries = e, page=page, offset=offset, prev_page = page-1, next_page = page+1)



class NewPostHandler(Handler):

    def get(self):
        self.render('new-post.html')

    def post(self):
        title = self.request.get("title")
        new_entry = self.request.get("new_entry")

        if not title or not new_entry:
            error = "Please provide a title and an entry."
            self.render('new-post.html', title=title, new_entry=new_entry, error=error)
        else:
            e = Entry(title=title, entry=new_entry)
            e.put()
            link_id = e.key().id()
            self.redirect('/blog/{}'.format(link_id))


class ViewPostHandler(Handler):
    def get(self, id):
        #self.write(id)
        #TODO:
        #Find webapp2 methods to return item using ID
        #new_entry = webapp2.methodThatReturnsID()
        e = Entry.get_by_id(int(id))
        #create new template, view-post.html which receives new_entry.title and new_entry.entry
        self.render("view-post.html", e=e)
        #render view-post.html


app = webapp2.WSGIApplication([
    ('/blog', MainHandler),
    ('/newpost', NewPostHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)

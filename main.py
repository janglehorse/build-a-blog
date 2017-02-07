# First, set up the blog so that the new post form and the post listing are on the same page,
# as with AsciiChan, and then separate those portions into separate routes, handler classes, and templates.
# For now, when a user submits a new post, redirect them to the main blog page.

# Make sure you can say the following about your app:
#
# The /blog route displays the 5 most recent posts. You'll need to filter the query results.
# You have two templates, one for each of the main blog and new post views.
# Your templates extend a base.html template which includes some boilerplate HTML that will be used on each page,
# along with some styles to clean up your blog's visuals a bit (you can copy/paste the styles from the AsciiChan exercise).
# You're able to submit a new post at the /newpost route/view.
# After submitting a new post, your app displays the main blog page. Note that, as with the AsciiChan example, you will likely need to refresh the main blog page to see your new post listed.
# If either title or body is left empty in the new post form, the form is rendered again,
# with a helpful error message and any previously-entered content in the same form inputs.
#

import os
import webapp2
import jinja2

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

class MainHandler(Handler):
    def get(self):
        self.render('new-post.html')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
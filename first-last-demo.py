#!/usr/bin/env python

appName = 'First Last Demo'


# - HTML Page Code

form_html = '''<style>
.form_wrap { margin-left: 55px; margin-top: 35px; outline: 1px solid #eee; width: 345px; padding: 45px; }
tr { height: 32px; }
td.label { font-size: 14px; text-align: right; padding-right: 10px; }
input[type="text"] { width: 200px; height: 16px; }
</style>
<div class="page_html">
  <article class="form_wrap">
    <form action="../../add_name" enctype="multipart/form-data" method="post">
      <table>
        <tr>
          <td class="label">First Name</td>
          <td class="input"><input type="text" name="first_name" /></td>
        </tr>
        <tr>
          <td class="label">Last Name</td>
          <td class="input"><input type="text" name="last_name" /></td>
        </tr>
        <tr>
          <td></td>
          <td style="text-align:right"><input type="submit" value="Enter Name" /></td>
        </tr>
      </table>
    </form>
  </article><!-- - /form_wrap - -->
</div><!-- - /page_html - -->'''


# - System
import os
import urllib
import wsgiref.handlers
import webapp2
import time
# -
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


class Name_db(db.Model):
    addTime = db.DateTimeProperty(auto_now_add=True)
  #
    first_name = db.StringProperty()
    last_name = db.StringProperty()

class addName_db(webapp2.RequestHandler):
    def post(self):
        item = Name_db()
      # - -
        item.first_name = self.request.get('first_name')
        item.last_name = self.request.get('last_name')
      #
        item.put()
        time.sleep(1)
        self.redirect('/')


class publicSite(webapp2.RequestHandler):
    def get(self):
      # - app data
        app = appName
        page_html = form_html

        q = db.Query(Name_db)
        names = q.fetch(100)

      # - template
        objects = {
            'app': app,
            'page_html': page_html,

            'names': names,
            
        }
      # - render
        path = os.path.join(os.path.dirname(__file__), 'html/publicSite.html')
        self.response.out.write(template.render(path, objects))


app = webapp2.WSGIApplication([    # - Pages
    ('/', publicSite),
    ('/add_name/?', addName_db),

], debug=True)


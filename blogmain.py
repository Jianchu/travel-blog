import os
import webapp2
import blogpage

app = webapp2.WSGIApplication([('/blog', blogpage.BlogPage)], debug=True)
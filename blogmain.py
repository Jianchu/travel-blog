import os
import webapp2
import blogpage
import signup

app = webapp2.WSGIApplication([('/blog', blogpage.BlogPage),('/',blogpage.BlogPage), ('/signup',signup.SignUp),('/welcome',signup.Welcome)], debug=True)
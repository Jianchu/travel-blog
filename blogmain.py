import os
import webapp2
import blogpage
import signup

app = webapp2.WSGIApplication([('/blog', blogpage.BlogPage),('/',blogpage.BlogPage), ('/signup',signup.SignUp),('/welcome/([a-zA-Z0-9_-]{3,20}$)',signup.Welcome),('/login',signup.Login)], debug=True)


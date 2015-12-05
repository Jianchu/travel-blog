import os
import webapp2
import blogpage
import logsystem

app = webapp2.WSGIApplication([('/blog', blogpage.BlogPage),('/',blogpage.BlogPage), ('/signup',logsystem.SignUp),('/welcome/([a-zA-Z0-9_-]{3,20}$)',logsystem.Welcome),('/login',logsystem.Login)], debug=True)


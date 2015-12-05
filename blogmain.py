import os
import webapp2
import blogpage
import logsystem
import personal
app = webapp2.WSGIApplication([('/blog', blogpage.BlogPage),('/',blogpage.BlogPage), ('/signup',logsystem.SignUp),('/welcome/([a-zA-Z0-9_-]{3,20}$)',logsystem.Welcome),('/login',logsystem.Login), ('/myblog/([a-zA-Z0-9_-]{3,20}$)', personal.PersonalPage)], debug=True)


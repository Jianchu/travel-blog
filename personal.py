from google.appengine.ext import db
import webapp2
import models
import handler
import re

class PersonalPage(handler.Handler):

	def get(self, username):
		username = self.request.cookies.get('username')
		if username:
			query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
			user = query.get() 	
			self.render("personalpage.html", username = user.username)
			return
		self.redirect("/signup")
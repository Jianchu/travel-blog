from google.appengine.ext import db
import models
import handler
import re

class PersonalPage(handler.Handler):

	def get(self, username):
		self.render("personalpage.html", username = username)
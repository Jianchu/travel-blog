import os
import webapp2
import handler
import blogutils
from google.appengine.ext import db
class BlogPage(handler.Handler):
	"""the main page of travel-blog"""
	def render_blogpage(self, username = ""):
		self.render("blogpage.html", username = username)

	def get(self):
		username = blogutils.checkcookie(self.request.cookies.get('username'))
		if username:
			self.render_blogpage(username)
			return
		self.render_blogpage()

		

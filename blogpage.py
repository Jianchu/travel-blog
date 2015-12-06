import os
import webapp2
import handler
import blogutils
from google.appengine.ext import db

class BlogPage(handler.Handler):
	"""the main page of travel-blog"""
	def render_blogpage(self, all_blogs = "", username = ""):
		self.render("blogpage.html", username = username, all_blogs = all_blogs)

	def get(self):
		all_blogs = blogutils.get_all_blogs()
		username = blogutils.checkcookie(self.request.cookies.get('username'))
		if username:
			self.render_blogpage(all_blogs,username)
			return
		self.render_blogpage(all_blogs)

		

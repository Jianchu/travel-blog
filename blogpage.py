import os
import webapp2
import handler

class BlogPage(handler.Handler):
	"""the main page of travel-blog"""
	def get(self):
		self.render("blogpage.html")
		

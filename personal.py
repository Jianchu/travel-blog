from google.appengine.ext import db
import webapp2
import models
import handler
import re
import blogutils

class PersonalPage(handler.Handler):

	def getCurrentUser(self):
		username = self.request.cookies.get('username')
		if username:
			query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
			user = query.get() 	
			return user.username

	def get(self, username):
		print username + "age"
		username = self.getCurrentUser()
		if username:
			blogs = blogutils.get_current_blogs(username)
			self.render("personalpage.html", username = username, blogs=blogs)
			return		
		self.redirect("/signup")


class NewPost(handler.Handler):

	def getCurrentUser(self):
		username = self.request.cookies.get('username')
		if username:
			query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
			user = query.get() 	
			return user.username

	def render_newpost(self, username = "", title = "", content = "", error = ""):
		self.render("newpost.html", username = username, title = title, content = content, error = error)

	def get(self, username):
		print username
		username = self.getCurrentUser()
		if username:
			self.render_newpost(username = username)
			return
		self.redirect("/signup")		

	def post(self,username):
		username = self.getCurrentUser()
		if username:			
			title = self.request.get("title")
			content = self.request.get("content")
			if (title and content):
				number_blog = blogutils.get_number_blog_current_user(username)
				new_blog = models.Blog(title = title, content = content, username = username, blog_id = username + "|"+ str(number_blog))
				old_num_blog = blogutils.get_number_blog_current_user(username)
				new_blog.put()
				blogutils.add_new_blog(username)
				while True:
					new_num_blog = blogutils.get_number_blog_current_user(username)		
					if old_num_blog != new_num_blog:
						break
				self.redirect("/myblog/%s" %str(username))
			else:
				error = "Subject and content, please!"
				self.render_newpost(username = username, title = title, content= content, error = error)
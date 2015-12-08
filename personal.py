from google.appengine.ext import db
import webapp2
import models
import handler
import re
import datetime
import blogutils

class PersonalPage(handler.Handler):

	def getCurrentUser(self):
		username = self.request.cookies.get('username')
		if username:
			query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
			user = query.get() 	
			return user.username

	def get(self, username):
		username = self.getCurrentUser()
		if username:
			blogs = blogutils.get_current_blogs(username)
			self.render("personalpage.html", username = username, blogs=blogs)
			return		
		self.redirect("/signup")

class NewEditPost(handler.Handler):

	def getCurrentUser(self):
		username = self.request.cookies.get('username')
		if username:
			query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
			user = query.get() 	
			return user.username

	def render_post(self, username = "", title = "", content = "", error = ""):
		self.render("newpost.html", username = username, title = title, content = content, error = error)

	def get(self, username):
		username = self.getCurrentUser()
		if username:
			self.render_post(username = username)
			return
		self.redirect("/signup")

	def post(self, username):
		username = self.getCurrentUser()
		if username:			
			title = self.request.get("title")
			content = self.request.get("content")
			blog_id = self.request.get("blog_id")
			if (title and content):
				old_num_blog = blogutils.get_number_blog_current_user(username)
				if blog_id:
					old_num_edition = blogutils.get_number_edition_current_blog(blog_id)
				edit_flag = self.new(title, content, username)
				new_flag = self.edit(blog_id, title, content)
				while new_flag:
					new_num_blog = blogutils.get_number_blog_current_user(username)		
					if old_num_blog != new_num_blog:
						break
				while edit_flag:
					new_num_edition = blogutils.get_number_edition_current_blog(blog_id)		
					if old_num_edition != new_num_edition:
						break
				self.redirect("/myblog/%s" %str(username))
			else:
				error = "Subject and content, please!"
				self.render_post(username = username, title = title, content= content, error = error)

	def new(self, title, content, username):
		return True

	def edit(self, blog_id, title, content):
		return True

class NewPost(NewEditPost):

	def new(this, title, content, username):
		number_blog = blogutils.get_number_blog_current_user(username)
		new_blog = models.Blog(title = title, content = content, username = username, number_of_edition = 0, blog_id = username + "_"+ str(number_blog))
		new_blog.put()
		blogutils.add_new_blog(username)
		return False

class EditPost(NewEditPost):

	def render_post(self, blog_id = "", username = "", title = "", content = "", error = ""):
		self.render("editpost.html", blog_id = blog_id, username = username, title = title, content = content, error = error)

	def get(self, blog_id):
		blog = blogutils.get_blog_by_id(blog_id)
		username = self.getCurrentUser()
		if username:
			self.render_post(blog_id = blog.blog_id, username = blog.username, title = blog.title, content = blog.content)
			return
		self.redirect("/signup")

	def edit(self, blog_id, title, content):
		blog = blogutils.get_blog_by_id(blog_id)
		blog.title = title
		blog.content = content
		blog.number_of_edition = blog.number_of_edition + 1
		blog.put()
		return False

class DeletePost(handler.Handler):

	def getCurrentUser(self):
		username = self.request.cookies.get('username')
		if username:
			query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
			user = query.get() 	
			return user.username

	def get(self, blog_id):
		blog = blogutils.get_blog_by_id(blog_id)
		username = self.getCurrentUser()
		if username:
			self.render("deletepost.html", blog = blog)
			return
		self.redirect("/signup")

	def post(self, blog_id):
		blog_id = self.request.get("blog_id")
		username = self.getCurrentUser()
		if blog_id:
			blogutils.delete_this_blog(blog_id)
		while True:
			blog = blogutils.get_blog_by_id(blog_id)
			if not blog:
				break	
		self.redirect("/myblog/%s" %str(username))			


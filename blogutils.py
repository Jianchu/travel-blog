from google.appengine.ext import db
import webapp2
import models

def checkcookie(username):
	print username
	if username:
		query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
		user = query.get() 
		return user.username
	return False

def get_total_user():
	return models.User.all().count()

def get_total_blog():
	return models.Blog.all().count()

def get_number_blog_current_user(username):
	query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
	user = query.get()
	return int(user.number_of_blog)

def get_current_user_id(username):
	query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
	user = query.get()
	return int(user.user_id)

def add_new_blog(username):
	query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
	user = query.get()
	user.number_of_blog = user.number_of_blog + 1
	user.put()

def get_current_blogs(username):
	return db.GqlQuery("SELECT * FROM Blog WHERE username = :username ORDER BY created DESC",username=username)

def get_all_blogs():
	return db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")		

def get_blog_by_id(blog_id):
	query = db.GqlQuery("SELECT * FROM Blog WHERE blog_id = :blog_id" ,blog_id=blog_id)
	return query.get()

def get_number_edition_current_blog(blog_id):
	query = db.GqlQuery("SELECT * FROM Blog WHERE blog_id = :blog_id" ,blog_id=blog_id)
	blog = query.get()
	return int(blog.number_of_edition)

def edit_old_blog(blog_id):
	query = db.GqlQuery("SELECT * FROM Blog WHERE blog_id = :blog_id" ,blog_id=blog_id)
	blog = query.get()
	blog.number_of_edition = blog.number_of_edition + 1
	blog.put()
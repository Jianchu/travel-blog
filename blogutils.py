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
	return user.number_of_blog

def get_current_user_id(username):
	query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
	user = query.get()
	return int(user.user_id)

def add_new_blog(username):
	query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
	user = query.get()
	user.number_of_blog = user.number_of_blog + 1
	user.put()
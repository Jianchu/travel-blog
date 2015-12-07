from google.appengine.ext import db

class User(db.Model):
	user_id = db.IntegerProperty(required = True)
	username = db.StringProperty(required = True)
	sign_up_time = db.DateTimeProperty(auto_now_add = True)
	password = db.TextProperty(required = True)
	email = db.StringProperty()
	number_of_blog = db.IntegerProperty(required = True)
	last_log_in_time = db.DateTimeProperty()
	last_log_in_place = db.StringProperty()

class Blog(db.Model):
	blog_id = db.StringProperty(required = True)
	username = db.StringProperty(required = True)
	title = db.StringProperty(required = True)	
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	number_of_edition = db.IntegerProperty(required = True)
from google.appengine.ext import db
import webapp2

def checkcookie(username):
	if username:
		query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
		user = query.get() 
		return user.username
	return False
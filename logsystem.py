from google.appengine.ext import db
import webapp2
import models
import handler
import re
import time
import blogutils 

USERNAME = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD = re.compile(r"^.{3,20}$")
EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$" )

def username_check(username):
	if (USERNAME.match(username)):
		return True
	return False

def username_exist_check(username):
	query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
	user = query.get()
	if user:
		return False
	return True

def password_check(password):
	if (PASSWORD.match(password)):
		return True
	return False 

def password_verify_check(password, password_verify):
	if (password == password_verify):
		return True
	return False

def email_check(email):
	if (EMAIL.match(email)):
		return True
	return False

def check_login(username, password):
	query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
	user = query.get()
	if user.password == password:
		return True
	return False


def get_total_user():
	return models.User.all().count()

class Welcome(handler.Handler):
	def get(self):
		username = blogutils.checkcookie(self.request.cookies.get('username'))
		if username:
			self.render("welcome.html", username = username)
			return
		self.redirect("/signup")

class Login(handler.Handler):
	def render_login(self, username = "", username_error = "", password_error = "", message = ""):
		self.render("login.html", username = username, username_error = username_error, password_error = password_error, message = message)

	def get(self):
		message = ""
		username = self.request.cookies.get('username')
		if username:
			query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
			user = query.get()
			message = "You have logged as %s, do you want to login another account?" % user.username  					
		self.render_login("","","",message)

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		username_error = ""
		password_error = ""
		error_flag = True
		if (not username_check(username)):
			username_error = "That's not a valid username."
			error_flag = False
		elif (username_exist_check(username)):
			username_error = "The user doesn't exist."
			error_flag = False			
		if (not password_check(password)):
			password_error = "That's not a valid password."
			error_flag = False
		elif ((not username_exist_check(username)) and (not check_login(username, password))):
			password_error = "The passowrd doesn't match the username."
			error_flag = False
		if (not error_flag): 
			self.render_login(username, username_error, password_error)
			return
		self.response.headers.add_header('Set-Cookie', 'username=%s' % str(username)) 
		self.redirect("/myblog/%s" % username)		

class Logout(handler.Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'username=')
		self.redirect("/blog")

class SignUp(handler.Handler):
	"""handle signup page"""

	def render_sign_up(self, username = "", email = "", username_error = "", password_error = "", password_verify_error = "", email_error = ""):
		self.render("signup.html", username = username, email = email, username_error = username_error, password_error = password_error, password_verify_error = password_verify_error, email_error = email_error)

	def get(self):
		self.render_sign_up()

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		password_verify = self.request.get('password_verify')
		email = self.request.get('email')

		username_error = ""
		password_error = ""
		password_verify_error = ""
		email_error = ""
		error_flag = True
		
		if (not username_check(username)):
			username_error = "That's not a valid username."
			error_flag = False
		if (not username_exist_check(username)):
			username_error = "The user already exists."
			error_flag = False
		if (not password_check(password)):
			password_error = "That's not a valid password."
			error_flag = False
		if (not password_verify_check(password, password_verify)):
			password_verify_error = "Your passwords doesn't match."
			error_flag = False
		if (not email_check(email) and len(email) > 0):
			email_error = "That's not a valid email."
			error_flag = False

		if (not error_flag):
			self.render_sign_up(username, email, username_error, password_error, password_verify_error, email_error)
			return
		key_mame = blogutils.get_total_user() + 1
		new_user = models.User(key_mame = str(username), user_id = key_mame, username = username, password = password, email = email, number_of_blog = 0)
		old_number_users = blogutils.get_total_user()
		new_user.put()
		self.response.headers.add_header('Set-Cookie', 'username=%s' % str(username))
		while True:
			new_number_users = blogutils.get_total_user()			
			if old_number_users != new_number_users:
				break
		self.redirect("/welcome")
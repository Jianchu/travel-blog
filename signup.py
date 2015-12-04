from google.appengine.ext import db
import models
import handler
import re

USERNAME = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD = re.compile(r"^.{3,20}$")
EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$" )

def username_check(username):
	if (USERNAME.match(username)):
		return True
	return False

def username_exist_check(username):
	query = db.GqlQuery("SELECT * FROM User WHERE username = :username",username=username)
	first = query.get()
	if first:
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

def get_total_user():
	return models.User.all().count()


class Welcome(handler.Handler):
	def get(self):
		self.render("welcome.html")


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
		new_user = models.User(key_mame = get_total_user() + 1, user_id = get_total_user() + 1, username = username, password = password, email = email)
		new_user.put()
		self.redirect("/welcome")
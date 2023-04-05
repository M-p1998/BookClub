from django.db import models
import re
import bcrypt

from django.utils import timezone
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, form):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(form['First_name']) < 2:
            errors["First_name"] = "First name should be at least 2 characters long."

        if len(form['Last_name']) < 2:
            errors["Last_name"] = "Last name should be at least 2 characters long."
        if not EMAIL_REGEX.match(form["Email"]):
            errors["Email"] = "Invalid email address."
        email_check = self.filter(email=form["Email"])
        if email_check:
            errors["Email"]= "Email is already in use!"

        if len(form['Password']) < 7:
            errors["Password"] = "Password must be at least 7 characters long."
        if form["Password"]!= form["confirm_password"]:
            errors["Password"] = "Passwords do not match."
        return errors

    def login_validator(self, postData):
        errors={}
        # filter = if user with this email in db exist
        email = User.objects.filter(email=postData["Email"])
        if not email:
            errors["creds"]="Invalid email/password!" 
        else: 
        # ensure that email is in db
            logged_user = email[0]
            # the password provide belongs to the user who owns the email
            if not bcrypt.checkpw(postData['Password'].encode(), logged_user.password.encode()):
                errors["creds"]="Invalid email/password!"
        return errors
           
class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()




from django.db import models

from login_app.models import User

class BookManager(models.Manager):
    def book_validator(self, post_data):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(post_data["Title"]) < 2:
            errors["Title"] = "Title should be at least 2 characters long."

        if len(Book.objects.filter(title = post_data['Title'])) > 0:
            errors['Title'] = 'This Title is already exist.'

        if len(post_data["Author"]) == 0:
            errors["Author"] = "Author name cannot be blank."
        elif len(post_data["Author"]) < 3:
            errors["Author"] = "Author name is too short."

        elif len(post_data["Author"]) < 5:
            errors["Author"] = "Author should be at least 5 characters long."
        
        if len(post_data["Description"]) < 7:
            errors["Description"] = "Description must be at least 7 characters long."
        
        return errors

class Book(models.Model):
    title = models.CharField(max_length=100)
    author=models.CharField(max_length=150)
    creator= models.ForeignKey(User,related_name="has_created_books", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_books")
    description = models.TextField()
    reviews_rating=None
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= BookManager()

class ReviewManager(models.Manager):
    def review_validator(self, form):
        errors={}
        if len(form["CONTENT"]) < 10:
            errors["CONTENT"] = "Review should be at least 10 characters long."
        if int(form["RATING"]) < 1 or int(form["RATING"]) > 5:
            errors["RATING"] = "Review should be 1 to 5 stars."
        return errors

class Review(models.Model):
    content=models.TextField()
    rating=models.IntegerField()
    book=models.ForeignKey(Book,related_name="reviews",on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name="user_create_reviews", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=ReviewManager()

    
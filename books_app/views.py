from django.shortcuts import render, redirect
from login_app.models import User
from .models import Book,Review
from django.contrib import messages

from django.db.models import Q

def dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")
    review=Review.objects.select_related("book").all()
    book = Book.objects.all()
    for all in book:
        total_rating = 0
        rating_count = 0
        for all_review in review:
            if all_review.book.id == all.id:
                rating_count += 1
                total_rating += all_review.rating
        
        if rating_count == 0:
            all.reviews_rating = 0
        else:
            all.reviews_rating = "{:.1f}".format(total_rating/rating_count) 
            
    context={
        "user":User.objects.get(id=request.session["user_id"]),
        "all_books":book      
    }
    return render(request, "dashboard.html", context)

def create_book(request):
    if "user_id" not in request.session:
        return redirect("/")
    book_errors = Book.objects.book_validator(request.POST)
    if len(book_errors) > 0:
        for key,value in book_errors.items():
            messages.error(request, value)
        return redirect(f"/books/add")
    else: 
        user=User.objects.get(id=request.session["user_id"])
        Book.objects.create(title=request.POST["Title"],author=request.POST["Author"],creator=user,description=request.POST["Description"])
        return redirect("/books/dashboard")

def add_books(request):
    if "user_id" not in request.session:
        return redirect("/")
    context= {
    "user":User.objects.get(id=request.session["user_id"])
    }
    return render(request, "add_book.html", context)

def view_book(request, book_id):
    if "user_id" not in request.session:
        return redirect("/")
    get_one_book={
        "one": Book.objects.get(id=book_id),
        "get_one":Review.objects.filter(book=Book.objects.get(id=book_id)),
        "current_user":User.objects.get(id=request.session["user_id"])
        # "one_user":User.objects.get(id=)
    }
    return render(request, "view.html",get_one_book)

def profile(request, user_id):
    if "user_id" not in request.session:
        return redirect("/")
    user = User.objects.get(id=user_id)
    reviews=user.user_create_reviews.all()
    context={
        "one_user":user,
        "reviews":reviews,
        "current_user":User.objects.get(id=request.session["user_id"])

    }
    return render(request, "profile.html", context)

def create_review(request,book_id):
    if "user_id" not in request.session:
        return redirect("/")
    review_errors = Review.objects.review_validator(request.POST)
    if len(review_errors) > 0:
        for key, value in review_errors.items():
            messages.error(request, value)
        return redirect(f"/books/view/{book_id}")
    else:
        Review.objects.create(content=request.POST["CONTENT"],rating=request.POST["RATING"],book=Book.objects.get(id=book_id),user=User.objects.get(id=request.session["user_id"]))
        return redirect(f"/books/view/{book_id}")

def update_book(request, book_id):
    if "user_id" not in request.session:
        return redirect("/")
    book=Book.objects.get(id=book_id)
    book.description=request.POST["description"]
    book.save()
    return redirect(f"/books/view/{book_id}")

def delete_review(request,review_id):
    if "user_id" not in request.session:
        return redirect("/")
    review_to_delete = Review.objects.get(id=review_id)
    review_to_delete.delete()
    return redirect(f"/books/view/{review_to_delete.book.id}")


def liked_book(request,book_id):
    book = Book.objects.get(id=book_id)
    user=User.objects.get(id=request.session["user_id"])
    user.favorited_books.add(book)
    return redirect(f"/books/view/{book_id}")

def unliked_book(request,book_id):
    book = Book.objects.get(id=book_id)
    user=User.objects.get(id=request.session["user_id"])
    user.favorited_books.remove(book)
    return redirect(f"/books/view/{book_id}")



def searchBook(request):
    if "user_id" not in request.session:
        return redirect("/")
    
    if request.method == "GET":
        search_query = request.GET.get("searched")
        if search_query:
        # Filter books that contain the query in either the title or author fields
            books = Book.objects.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
            if not books:
                return redirect(f"/books/noBookFound")
        else:
            books = Book.objects.none()

    for book in books:
        reviews = Review.objects.filter(book=book)
        total_rating = 0
        rating_count = 0
        for review in reviews:
            rating_count += 1
            total_rating += review.rating
            
        if rating_count == 0:
            book.reviews_rating = 0
        else:
            book.reviews_rating = "{:.1f}".format(total_rating/rating_count)

    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "query": search_query,
        "books": books
    }

    return render(request, "searchResult.html", context)

def no_book_found(request):
    # return render(request, "noBook.html")
    return render(request, "searchResult.html")




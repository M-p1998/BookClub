from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard),
    path("create/book",views.create_book),
    path("add",views.add_books),
    path("view/<int:book_id>",views.view_book),
    path("users/<int:user_id>", views.profile),
    path("add/review/<int:book_id>",views.create_review),
    path("delete/<int:review_id>",views.delete_review),
    path("like/<int:book_id>",views.liked_book),
    path("unlike/<int:book_id>",views.unliked_book),
    # path("edit/<int:book_id>",views.edit_book),
    path("update/<int:book_id>",views.update_book),
    path("search",views.searchBook),
    path("noBookFound",views.no_book_found)
    
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("addbook", views.AddBookView, name="addbook"),
    path("searchResults/", views.SearchResultsView, name="searchResults"),
    path("newDiscussion/", views.NewDiscussionView, name="newDiscussion"),
    path("newBook/", views.NewBookView, name="newBook"),
    path("newPost/<str:bookId>", views.NewPostView, name="newPost"),
    path("newPost/", views.NewPostView, name="newPost"),
    path("discussion/<str:bookId>", views.DiscussionView, name="discussion")
]

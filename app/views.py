from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from urllib.parse import urlencode
from .forms import UserSignupForm
from app.models import Book
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Create your views here.
def index(request):
    return render(request, "index.html")

def AddBookView(request):
    return render(request, "addbook.html")

def SearchResultsView(request):
    base_url = "https://www.googleapis.com/books/v1/volumes?"
    params = {
        'q': request.GET['title'] + ' inauthor:' + request.GET['author'], 
        'key': os.environ.get('API_KEY'),
        'maxResults': 40
    }
    url = base_url + urlencode(params)

    try:
        response = requests.get(url)
        response_json = response.json()
        bookList = []

        if len(response_json['items']) > 0:
            for i in range(len(response_json['items'])):
                volumeInfo = response_json['items'][i]['volumeInfo'] if 'volumeInfo' in response_json['items'][i] else ''
                bookInfo = {
                    "title": volumeInfo['title'] if 'title' in volumeInfo else 'No title listed',
                    "author": volumeInfo['authors'][0] if 'authors' in volumeInfo and (len(volumeInfo['authors']) > 0) else 'No author listed',
                    "description": volumeInfo['description'] if 'description' in volumeInfo else 'No description listed',
                    "thumbnail": volumeInfo['imageLinks']['thumbnail'] if ('imageLinks' in volumeInfo and 'thumbnail' in volumeInfo['imageLinks']) else None,
                    "language": volumeInfo['language'] if 'language' in volumeInfo else 'No language listed',
                    "bookId": response_json['items'][i]['id']
                }
                bookList.append(bookInfo)
            return render(request, "searchResults.html", { "searchResult": bookList })
        else:
            print("No results found")
            return render(request, "searchResults.html", { "searchResult": None })
        
    except (Exception):
        return render(request, "error.html")
    

def NewDiscussionView(request):
    title = request.POST['title']
    author = request.POST['author']
    description = request.POST['description']
    thumbnail = request.POST['thumbnail']
    bookId = request.POST['bookId']
    return render(request, "postForm.html", {
        "title": title, 
        "author": author, 
        "description": description, 
        "thumbnail": thumbnail,
        "bookId": bookId
    })

def NewBookView(request):
    title = request.POST['title']
    author = request.POST['author']
    description = request.POST['description']
    thumbnail = request.POST['thumbnail']
    bookId = request.POST['bookId']
    newBook = Book(title=title, author=author, description=description, thumbnail=thumbnail, bookId=bookId)
    newBook.save()
    print("Redirecting home...")
    return redirect(reverse("home"))

def NewCommentView(request):
    postTitle = request.POST['postTitle']
    postText = request.POST['postText']
    pass

class SignUpView(generic.CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

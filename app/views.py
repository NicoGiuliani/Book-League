import json
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from urllib.parse import urlencode
from .forms import UserSignupForm
from app.models import Book, Post
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
                book = {
                    "title": volumeInfo['title'] if 'title' in volumeInfo else 'No title listed',
                    "author": volumeInfo['authors'][0] if 'authors' in volumeInfo and (len(volumeInfo['authors']) > 0) else 'No author listed',
                    "description": volumeInfo['description'] if 'description' in volumeInfo else 'No description listed',
                    "thumbnail": volumeInfo['imageLinks']['thumbnail'] if ('imageLinks' in volumeInfo and 'thumbnail' in volumeInfo['imageLinks']) else None,
                    "language": volumeInfo['language'] if 'language' in volumeInfo else 'No language listed',
                    "bookId": response_json['items'][i]['id']
                }
                bookList.append(book)

            # All the book IDs returned in this search
            bookIds = list(map(lambda book: book['bookId'], bookList))

            # All books in the database that showed up in this search
            booksInDb = Book.objects.filter(bookId__in=bookIds)
            booksInDbList = list(booksInDb)

            idsInDb = list(map(lambda book: book.bookId, booksInDbList))
            filteredList = list(filter(lambda book: book['bookId'] not in idsInDb, bookList))

            return render(request, "searchResults.html", { "booksInDatabase": booksInDb, "searchResult": filteredList })
        else:
            print("No results found")
            return render(request, "searchResults.html", { "searchResult": None })
        
    except (Exception):
        return render(request, "error.html")
    

def NewDiscussionView(request):
    title = request.POST["title"]
    author = request.POST["author"]
    description = request.POST["description"]
    thumbnail = request.POST["thumbnail"]
    bookId = request.POST["bookId"]
    return render(request, "postForm.html", {
        "title": title, 
        "author": author, 
        "description": description, 
        "thumbnail": thumbnail,
        "bookId": bookId
    })

def NewBookView(request):
    newBook = {
        "title": request.POST['title'],
        "author": request.POST['author'],
        "description": request.POST['description'],
        "thumbnail": request.POST['thumbnail'],
        "bookId": request.POST['bookId'],
    }

    book = Book(
        title=newBook["title"], 
        author=newBook["author"], 
        description=newBook["description"], 
        thumbnail=newBook["thumbnail"], 
        bookId=newBook["bookId"]
        )
    book.save()

    request.session['redirectFromNewBook'] = True
    request.session['postTitle'] = request.POST['postTitle']
    request.session['postText'] = request.POST['postText']
    request.session['book'] = newBook
    return redirect(reverse("newPost"))

def NewPostView(request, bookId=None):
    if bookId is not None:
        print("Writing a post for an existing book...")
        book = Book.objects.filter(bookId=bookId).first()
        return render(request, "postForm.html", {
            "title": book.title, 
            "author": book.author, 
            "description": book.description, 
            "thumbnail": book.thumbnail,
            "bookId": book.bookId
        })
    elif (request.session['redirectFromNewBook']):
        print("Writing a post for a newly added book...")
        postTitle = request.session.get('postTitle')
        postText = request.session.get('postText')
        book = request.session.get('book')
        bookId = book['bookId']

        newPost = Post(postTitle=postTitle, postText=postText, bookId=bookId)

        # Clear session variables
        request.session['redirectFromNewBook'] = False
        request.session['postTitle'] = None
        request.session['postText'] = None
        request.session['book'] = None
    else:
        print("An error may have occurred")
        pass

    newPost.save()
    return redirect(reverse("discussion", args=(bookId,)))

def DiscussionView(request, bookId):
    book = Book.objects.filter(bookId=bookId).first()
    posts = Post.objects.filter(bookId=book.bookId)
    return render(request, "discussion.html", {"book": book, "posts": posts})

class SignUpView(generic.CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

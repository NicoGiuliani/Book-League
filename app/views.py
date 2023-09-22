from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from urllib.parse import urlencode
from .forms import UserSignupForm
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
    params = {'q': request.GET['title'], 'inauthor': request.GET['author'], 'key': os.environ.get('API_KEY')}

    try:
        response = requests.get(base_url, params=params)
        response_json = response.json()
        bookList = []
        print(response_json['totalItems'])

        if response_json['totalItems'] > 0:
            for i in range(response_json['totalItems']):
                print("i:", i)
                volumeInfo = response_json['items'][i]['volumeInfo']
                print(volumeInfo)
                bookInfo = {
                    "title": volumeInfo['title'],
                    "author": volumeInfo['authors'][0],
                    "description": volumeInfo['description'],
                    "thumbnail": volumeInfo['imageLinks']['thumbnail'] if ('imageLinks' in volumeInfo and 'thumbnail' in volumeInfo['imageLinks']) else None,
                    "language": volumeInfo['language']
                }
                print("got book info")
                bookList.append(bookInfo)
                print("bookList length:", len(bookList))
                if len(bookList) == 5:
                    print("Reached length 5")
                    print("final bookList:", bookList)
                    break
            print("rendering...")
            return render(request, "searchResults.html", { "searchResult": bookList })
        else:
            print("No results found")
            return render(request, "searchResults.html", { "searchResult": None })
        
    except (Exception):
        return render(request, "error.html")
    

class SignUpView(generic.CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"



# def login(request):
#     return render(request, 'login.html')

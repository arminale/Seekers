# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Book
from django.utils import timezone
from isbnlib import meta, is_isbn10, is_isbn13
import isbnlib

SERVICE = 'openl'

# Create your views here.
def index(request):

    returns = {}

    categories = list(set(Book.objects.all().values_list('category', flat=True)))
    returns['categories'] = categories




    if request.method == "POST":
        print request.POST
        searchTerm = request.POST.get('search_term')
        returns['search_term'] = searchTerm
        if searchTerm != "" and searchTerm != None:

                results = Book.objects.filter(book_name__startswith=searchTerm)

                found_results = len(results) != 0
                returns['found_results'] = found_results
                print results
                if found_results:
                    returns['results'] = results

        if request.POST.get('add_button') != None:
            if request.POST.get('Title') == "" or request.POST.get('Title') == None or request.POST.get('Author') == "" or request.POST.get('Author') == None or request.POST.get('Quantity') == 0 or request.POST.get('Quantity') == None or request.POST.get('Category') == "" or request.POST.get('Category') == None:
                metadata = { 'Title': request.POST.get('Title'), 'Author' : request.POST.get('Author'), 'Category' :request.POST.get('Category'), 'Quantity' : request.POST.get('Quantity') }
                returns['metadata'] = metadata
            else:
                try:
                    book = Book.objects.get(book_name=request.POST.get('Title'))
                except:
                    book = Book()
                    book.date_added = timezone.now()
                book.book_name = request.POST.get('Title')
                book.author = request.POST.get('Author')
                book.quantity = request.POST.get('Quantity')
                book.category = request.POST.get('Category')
                

                book.save()


        elif request.POST.get('lookup') != None:
            isbn = request.POST.get('ISBN')

            if is_isbn10(isbn) or is_isbn13(isbn):

                try:
                    metadata = meta(isbn)
                    clean_metadata = {'Author': metadata.get('Authors')[0], 'Title': metadata.get('Title'), 'ISBN' : isbn }
                    returns['isbnFound'] = True
                    returns['metadata'] =  clean_metadata

                except:

                    clean_metadata = { 'ISBN' : isbn }
                    returns['isbnFound'] = False
                    returns['metadata'] =  clean_metadata
            else:

                clean_metadata = { 'ISBN' : isbn }
                returns['isbnFound'] = False
                returns['metadata'] =  clean_metadata
        elif request.POST.get('search') != None:
            searchTerm = request.POST.get('search_term')

            returns['search_term'] = searchTerm
            if searchTerm != "":

                results = Book.objects.filter(book_name__startswith=searchTerm)

                found_results = len(results) != 0
                returns['found_results'] = found_results
                if found_results:
                    returns['results'] = results
        elif request.POST.get('addnew') != None:
            metadata = {'Title' : searchTerm}
            returns['metadata'] = metadata
        
        else:
            for key in request.POST.keys():
                if key.isnumeric():
                    bookKey = key
                    break
            if request.POST.get(bookKey) == "+":
                book = Book.objects.get(pk=bookKey)
                book = Book.objects.get(pk=bookKey)
                book.quantity += 1
                book.save()
                returns['results'] = None
                returns['search_term'] = ""
            elif request.POST.get(bookKey) == "-":
                book = Book.objects.get(pk=bookKey)
                book.quantity -= 1
                book.save()
                returns['results'] = None
                returns['search_term'] = ""
            else:
                book = Book.objects.get(pk=bookKey)

                metadata = {'Title' : book.book_name, 'Author' : book.author, 'Quantity' : book.quantity, 'Category': book.category}
                returns['metadata'] = metadata

    return render(request, 'inventory/index.html', returns)

# def detail(request, book_id):
    # book = get_object_or_404(Book, pk = book_id)
    # if request.method == "POST":
        # book.book_name = request.POST.get('book_name')
        # book.author = request.POST.get('author')
        # book.quantity = request.POST.get('quantity')
        # if request.POST.get('isbn') != None:
            # book.isbn = request.POST.get('isbn')
        # else:
            # book.isbn = 0
        # book.category = request.POST.get('category')
        # book.save()
    # return render(request, 'inventory/detail.html', {'book':book})

# def search(request,searchTerm = ""):
    # results = None
    # found_results = None
    # if request.method=="POST":
        # searchTerm = request.POST.get('search_box')

        # if request.POST.get('search_button') != None:
            # if searchTerm != "":
                # results = Book.objects.filter(book_name__startswith=searchTerm)
                # found_results = len(results) != 0
            # return render(request,'inventory/search.html', {'search_term' : searchTerm, 'results' :results, 'found_results': found_results})
        # elif request.POST.get('add_button') != None:
            # searchTerm = searchTerm.replace(" ", "_")
            # return HttpResponseRedirect(reverse('inventory:add', args=(searchTerm,)))
    # else:
        # return render(request,'inventory/search.html', {'search_term' : searchTerm})


# def add(request, searchTerm= ""):
    # searchTerm = searchTerm.replace("_", " ")
    # if request.method=="POST":
        # book = Book()
        # book.book_name = request.POST.get('book_name')
        # book.author = request.POST.get('author')
        # book.quantity = request.POST.get('quantity')
        # book.date_added = timezone.now()
        # book.save()
        # if request.POST.get('add_another') != None:
            # return render(request,'inventory/add.html')
        # elif request.POST.get('add_back') != None:
            # return HttpResponseRedirect(reverse('inventory:search'))
        # elif request.POST.get('look_up') != None:
            # isbn = request.POST.get('isbn')
            # if is_isbn10(isbn) or is_isbn13(isbn):
                # metadata = meta(request.POST.get('isbn'), SERVICE)
                # clean_metadata = {'Author': metadata.get('Authors')[0], 'Title': metadata.get('Title'), 'ISBN' : isbn }
                # return render(request, 'inventory/add.html', {'isbnFound' : True, 'metadata': clean_metadata})
            # else:
                # clean_metadata = { 'ISBN' : isbn }
                # return render(request, 'inventory/add.html', {'isbnFound' : False, 'metadata': clean_metadata})

    # else:
        # return render(request,'inventory/add.html', {'search_term' : searchTerm})

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
    categories = list(set(Book.objects.all().values_list('category', flat=True)))
    print categories
    if request.method == "POST":
        if request.POST.get('add_button') != None:
            book = Book()
            book.book_name = request.POST.get('book_name')
            book.author = request.POST.get('author')
            book.quantity = request.POST.get('quantity')
            book.date_added = timezone.now()
            book.save()
            
        elif request.POST.get('lookup') != None:
            isbn = request.POST.get('ISBN')
            if is_isbn10(isbn) or is_isbn13(isbn):
            
                try:
                    metadata = meta(isbn)
                    
                except:
                    print metadata
                    clean_metadata = { 'ISBN' : isbn }
                    return render(request, 'inventory/index.html', {'isbnFound' : False, 'metadata': clean_metadata})
                    
                    
                clean_metadata = {'Author': metadata.get('Authors')[0], 'Title': metadata.get('Title'), 'ISBN' : isbn }
                return render(request, 'inventory/index.html', {'isbnFound' : True, 'metadata': clean_metadata})
            else:
                
                clean_metadata = { 'ISBN' : isbn }
                return render(request, 'inventory/index.html', {'isbnFound' : False, 'metadata': clean_metadata})
    return render(request, 'inventory/index.html', {'categories': categories})
    
def detail(request, book_id):
    book = get_object_or_404(Book, pk = book_id)
    if request.method == "POST":
        book.book_name = request.POST.get('book_name')
        book.author = request.POST.get('author')
        book.quantity = request.POST.get('quantity')
        if request.POST.get('isbn') != None:
            book.isbn = request.POST.get('isbn')
        else:
            book.isbn = 0
        book.category = request.POST.get('category')
        book.save()
    return render(request, 'inventory/detail.html', {'book':book})

def search(request,searchTerm = ""):
    results = None
    found_results = None
    if request.method=="POST":
        searchTerm = request.POST.get('search_box')

        if request.POST.get('search_button') != None:
            if searchTerm != "":
                results = Book.objects.filter(book_name__startswith=searchTerm)
                found_results = len(results) != 0
            return render(request,'inventory/search.html', {'search_term' : searchTerm, 'results' :results, 'found_results': found_results})
        elif request.POST.get('add_button') != None:
            searchTerm = searchTerm.replace(" ", "_")
            return HttpResponseRedirect(reverse('inventory:add', args=(searchTerm,)))
    else:
        return render(request,'inventory/search.html', {'search_term' : searchTerm})
    

def add(request, searchTerm= ""):
    searchTerm = searchTerm.replace("_", " ")
    if request.method=="POST":
        book = Book()
        book.book_name = request.POST.get('book_name')
        book.author = request.POST.get('author')
        book.quantity = request.POST.get('quantity')
        book.date_added = timezone.now()
        book.save()
        if request.POST.get('add_another') != None:
            return render(request,'inventory/add.html')
        elif request.POST.get('add_back') != None:
            return HttpResponseRedirect(reverse('inventory:search'))
        elif request.POST.get('look_up') != None:
            isbn = request.POST.get('isbn')
            if is_isbn10(isbn) or is_isbn13(isbn):
                metadata = meta(request.POST.get('isbn'), SERVICE)
                clean_metadata = {'Author': metadata.get('Authors')[0], 'Title': metadata.get('Title'), 'ISBN' : isbn }
                return render(request, 'inventory/add.html', {'isbnFound' : True, 'metadata': clean_metadata})
            else:
                clean_metadata = { 'ISBN' : isbn }
                return render(request, 'inventory/add.html', {'isbnFound' : False, 'metadata': clean_metadata})
            
    else:
        return render(request,'inventory/add.html', {'search_term' : searchTerm})
    
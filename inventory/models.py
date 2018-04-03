# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Book(models.Model):
    book_name = models.CharField(max_length = 400)
    author = models.CharField(max_length = 200)
    date_added = models.DateTimeField()
    quantity = models.IntegerField(default = 0)
    category = models.CharField(max_length = 200)
    isbn = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.book_name
    
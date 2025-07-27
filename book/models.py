from django.db import models
from django.contrib.auth.models import User
class Author(models.Model):
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=80)
    bio=models.CharField(max_length=80)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Genre(models.Model):
    name=models.CharField(max_length=255,unique=True)


class Book(models.Model):
    title=models.CharField(max_length=100)
    authors=models.ManyToManyField(Author)
    genres=models.ManyToManyField(Genre)
    publication_date=models.DateField()
    pages=models.IntegerField()
    in_stock=models.BooleanField(default=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    rating=models.IntegerField(choices=[(i,i) for i in range(1,6)])
    review=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import *
from django.shortcuts import get_object_or_404
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

@api_view(['GET','POST'])
def author_list(request):
    if request.method=='GET':
        author=Author.objects.all()
        serializers=AuthorSerializer(author,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        serializers=AuthorSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response({'error':'Invalid request'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def author_details(request,pk):
    author=get_object_or_404(Author,pk=pk)
    if request.method=='GET':
        serializers=AuthorSerializer(author)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method=='PUT':
        serializers=AuthorSerializer(author)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_404_BAD_REQUEST)
    elif request.method=='DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def genre_list(request):
    if request.method=='GET':
        author=Genre.objects.all()
        serializers=GenreSerializer(author,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        serializers=GenreSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response({'error':'Invalid request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def genre_details(request,pk):
    genre=get_object_or_404(Genre,pk=pk)
    if request.method=='GET':
        serializers=GenreSerializer(genre)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method=='PUT':
        serializers=GenreSerializer(genre)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_404_BAD_REQUEST)
    elif request.method=='DELETE':
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def book_list(request):
    if request.method=='GET':
        book=Book.objects.all()

        filtered_books=BookFilter(request.GET,queryset=book).qs

        paginator=PageNumberPagination()
        paginated_books=paginator.paginate_queryset(filtered_books,request)
        serializers=BookSerializer(paginated_books,many=True)
        return paginator.get_paginated_response(serializers.data)
        
    elif request.method=='POST':
        serializers=BookSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(created_by=request.user)
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response({'error':'Invalid request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def book_details(request,pk):
    book=get_object_or_404(Book,pk=pk)
    if request.method=='GET':
        serializers=BookSerializer(book)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    if request.method=='PUT':
        if request.user !=book.created_by:
            return Response({'error':'You are not allowed to modify this book'})
        serializers=BookSerializer(book)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_404_BAD_REQUEST)
    elif request.method=='DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def review_list(request):
    if request.method=='GET':
        review=Review.objects.all()
        serializers=ReviewSerializer(review,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        serializers=ReviewSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=request.user)
            return Response(serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response({'error':'Invalid request'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def review_details(request,pk):
    review=get_object_or_404(Review,pk=pk)
    if request.method=='GET':
        serializers=ReviewSerializer(review)
        return Response(serializers.data,status=status.HTTP_200_OK)
   
    if request.method=='PUT':
        if request.user!=review.user:
            return Response({'error':'You are not allowed to modify this review'})
        serializers=ReviewSerializer(review)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_404_BAD_REQUEST)
    elif request.method=='DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
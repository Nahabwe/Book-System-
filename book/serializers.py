from .models import Review,Book,Author,Genre
from django.contrib.auth.models import User
from rest_framework import serializers



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'

class AuthorFullNameField(serializers.SlugRelatedField):
    def to_internal_value(self,data):
        try:
            first_name,last_name=data.split(' ',1)
        except ValueError:
            raise serializers.ValidationError('Full name must include first and last name')
        try:
            return Author.objects.get(first_name=first_name,last_name=last_name)
        except Author.DoesNotExist:
            raise serializers.ValidationError('Author with this full does not exist')
    def to_representation(self, obj):
        return f'{obj.first_name} {obj.last_name}'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields='__all__'

class BookSerializer(serializers.ModelSerializer):
    authors=AuthorFullNameField(
        many=True,
        slug_field='full_name',
        queryset=Author.objects.all()
    )
    genres=serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Genre.objects.all())
    created_by=serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model=Book
        fields=['id','title','authors','genres','publication_date','pages','in_stock','created_by','created_at']
        read_only_fields = ['created_by', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    book=serializers.SlugRelatedField(
        slug_field='title',
        queryset=Book.objects.all())
    user=serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)
  

    class Meta:
        model=Review
        fields=['id','book','user','rating','review','created_at']
        read_only_fields=['created_at','user']

from .models import Book
import django_filters

class BoookFilter(django_filters.FilterSet):
    title=django_filters.CharFielter(field_name='title',look_expr='icontains')
    author=django_filters.CharFilter(method='filter_author')
    genre=django_filters.CharFilter(filed_name='genre__name',look_expre='icontains')

    class Meta:
        model=Book
        fileds=['totle','author','genre']
    def filter_author(self,queryset,name,value):
        try:
            first,last=value.splait(' ',1)
            return queryset.filter(authors__first_name__iexact=first,authors__last_name__iexact=last)
        except ValueError:
            return queryset.one()
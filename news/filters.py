from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post


class PostFilter(FilterSet):
    # позже указываемой даты
    posted_after = DateTimeFilter(
        field_name='post_date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%d.%m.%Y %H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
       model = Post
       fields = {
           # поиск по типу публикации
           'post_type': ['exact'],
           # поиск по названию
           'post_title': ['icontains'],
           # поиск по категории
           'post_category': ['exact'],
       }

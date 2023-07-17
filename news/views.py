from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'post_date'
    template_name = 'NewsList.html'
    context_object_name = 'newslist'


class NewsDetail(DetailView):
    model = Post
    template_name = 'NewsDetail.html'
    context_object_name = 'news'

from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)


class NewsList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'NewsList.html'
    context_object_name = 'newslist'
    paginate_by = 10


class NewsSearch(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'NewsSearch.html'
    context_object_name = 'newslist'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'NewsDetail.html'
    context_object_name = 'news'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "NW"
        return super().form_valid(form)


class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "AR"
        return super().form_valid(form)


class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class ArticlesEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')

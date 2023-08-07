from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Post, Author, Subscriber, Category
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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "NW"
        try:
            auth = Author.objects.get(author_user=self.request.user)
        except ObjectDoesNotExist:
            auth = Author.objects.create(author_user=self.request.user)
        post.post_author = auth
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "AR"
        try:
            auth = Author.objects.get(author_user=self.request.user)
        except ObjectDoesNotExist:
            auth = Author.objects.create(author_user=self.request.user)
        post.post_author = auth
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    context_object_name = 'news'


class ArticlesEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    context_object_name = 'news'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

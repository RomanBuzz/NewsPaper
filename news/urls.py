from django.urls import path
from .views import (
   NewsList, NewsSearch, NewsDetail,
   NewsCreate, NewsEdit, NewsDelete,
   ArticlesCreate, ArticlesEdit, ArticlesDelete
)

urlpatterns = [
   path('', NewsList.as_view(), name='post_list'),
   path('<int:pk>', NewsDetail.as_view(), name='post_detail'),
   path('search/', NewsSearch.as_view(), name='post_search'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
]

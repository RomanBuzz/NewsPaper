from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):

        # post_rat - суммарный рейтинг каждой статьи автора умножается на 3
        # post_comment_rat - суммарный рейтинг всех комментариев к статьям автора
        post_rat = 0
        post_comment_rat = 0
        for p_rat in self.post_set.all():
            post_rat += p_rat.post_rating
            for c_rat in p_rat.comment_set.all():
                post_comment_rat += c_rat.comment_rating

        # comment_rat - суммарный рейтинг всех комментариев автора
        comment_rat = 0
        for c_rat in self.author_user.comment_set.all():
            comment_rat += c_rat.comment_rating

        self.author_rating = post_rat * 3 + comment_rat + post_comment_rat
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.category_name.title()


class Post(models.Model):
    news = 'NW'
    article = 'AR'

    CATEGORIES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,
                                 choices=CATEGORIES,
                                 default=news)
    post_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:123] + "..." if len(str(self.post_text)) > 124 else self.post_text

    def __str__(self):
        return f'{self.post_title.title()} :: ' \
               f'{self.post_date.strftime("%d.%m.%Y %H:%M:%S")} :: ' \
               f'{self.post_text[0:123] + "..." if len(str(self.post_text)) > 124 else self.post_text}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

from news.models import *

# Создать двух пользователей (с помощью метода User.objects.create_user('username')).
u1 = User.objects.create_user(username='Пользователь 1')
u2 = User.objects.create_user(username='Пользователь 2')

# Создать два объекта модели Author, связанные с пользователями.
a1 = Author.objects.create(author_user=u1)
a2 = Author.objects.create(author_user=u2)

# Добавить 4 категории в модель Category.
Category.objects.create(category_name="Medicine")
Category.objects.create(category_name="Travelling")
Category.objects.create(category_name="Technologies")
Category.objects.create(category_name="Science")

# Добавить 2 статьи и 1 новость.
Post.objects.create(post_author=a1, post_type="NW", post_title="Post1", post_text="Post1 text")
Post.objects.create(post_author=a1, post_type="AR", post_title="Post2", post_text="Post2 text")
Post.objects.create(post_author=a2, post_type="AR", post_title="Post3", post_text="Post3 text")

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
Post.objects.get(id=1).post_category.add(Category.objects.get(pk=1))
Post.objects.get(id=2).post_category.add(Category.objects.get(pk=2))
Post.objects.get(id=2).post_category.add(Category.objects.get(pk=3))
Post.objects.get(id=3).post_category.add(Category.objects.get(pk=2))
Post.objects.get(id=3).post_category.add(Category.objects.get(pk=3))
Post.objects.get(id=3).post_category.add(Category.objects.get(pk=4))

# Создать как минимум 4 комментария к разным объектам модели Post
# (в каждом объекте должен быть как минимум один комментарий).
Comment.objects.create(comment_post=Post.objects.get(id=1),
                       comment_user=Author.objects.get(id=1).author_user, comment_text="Comment text 1")
Comment.objects.create(comment_post=Post.objects.get(id=2),
                       comment_user=Author.objects.get(id=1).author_user, comment_text="Comment text 2")
Comment.objects.create(comment_post=Post.objects.get(id=2),
                       comment_user=Author.objects.get(id=2).author_user,
                       comment_text="Comment text 3")
Comment.objects.create(comment_post=Post.objects.get(id=3),
                       comment_user=Author.objects.get(id=2).author_user, comment_text="Comment text 4")

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Post.objects.get(id=1).like()
Post.objects.get(id=1).like()
Post.objects.get(id=1).like()
Post.objects.get(id=1).dislike()

Post.objects.get(id=2).like()
Post.objects.get(id=2).like()
Post.objects.get(id=2).like()
Post.objects.get(id=2).like()
Post.objects.get(id=2).dislike()

Post.objects.get(id=3).like()
Post.objects.get(id=3).like()
Post.objects.get(id=3).like()
Post.objects.get(id=3).like()
Post.objects.get(id=3).like()
Post.objects.get(id=3).dislike()

Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).dislike()

Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).dislike()

Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).dislike()

Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).dislike()

# Обновить рейтинги пользователей.
Author.objects.get(id=1).update_rating()
Author.objects.get(id=2).update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
a = Author.objects.order_by('-author_rating')[0]
a.author_user.username
a.author_rating

# Вывести дату добавления, username автора, рейтинг,
# заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
a.author_user.date_joined.strftime("%d.%m.%Y %H:%M:%S")
a.author_user.username
a.author_rating
best_post = a.post_set.all().order_by('-post_rating')[0]
best_post.post_title
best_post.preview()

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
best_post_comments = best_post.comment_set.all()
for cm in best_post_comments:
    cm.comment_date.strftime("%d.%m.%Y %H:%M:%S")
    cm.comment_user
    cm.comment_rating
    cm.comment_text

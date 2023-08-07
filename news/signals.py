from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, PostCategory


def send_msg(category, post_title, post_type, post_url, emails):
    subject = f'Новая публикация в категории {category}'

    text_content = (
        f'Название: {post_title}\n'
        f'Тип: {post_type}\n'
        f'Категория: {category}\n\n'
        f'Ссылка на публикацию: http://127.0.0.1:8000{post_url}'
    )
    html_content = (
        f'Название: {post_title}<br>'
        f'Тип: {post_type}<br>'
        f'Категория: {category}<br><br>'
        f'<a href="http://127.0.0.1:8000{post_url}">'
        f'Ссылка на публикацию</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=PostCategory)
def post_created(instance, created, **kwargs):
    if not created:
        return

    # print('test 1:', instance.post.post_title, '||', instance.post.get_post_type_display(), '||',
    #       instance.category, '||', instance.post.get_absolute_url())

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True).distinct()

    send_msg(instance.category.category_name, instance.post.post_title, instance.post.get_post_type_display(),
             instance.post.get_absolute_url(), emails)


@receiver(m2m_changed, sender=Post.post_category.through)
def category_saved(instance, action, **kwargs):
    if action != 'post_add':
        return

    category_str = '|'.join(instance.post_category.all().values_list('category_name', flat=True))

    # print('test 2:', instance.post_title, '||', instance.get_post_type_display(), '||',
    #       category_str, '||', instance.get_absolute_url())

    emails = User.objects.filter(
        subscriptions__category__in=instance.post_category.all()
    ).values_list('email', flat=True).distinct()

    send_msg(category_str, instance.post_title, instance.get_post_type_display(),
             instance.get_absolute_url(), emails)

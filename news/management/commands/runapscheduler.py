import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from news.models import Post, Category, Mailing

logger = logging.getLogger(__name__)


def my_job():
    for user in User.objects.exclude(email__isnull=True).exclude(email=''):

        user_category = Category.objects.filter(pk__in=user.subscriptions.all().values_list('category', flat=True))
        user_cat_str = '|'.join(user_category.values_list('category_name', flat=True))

        # print('test 3: ', user.username, '||', user_category, '||', user_cat_str)

        request_period = datetime.now() - timedelta(days=7)

        news = Post.objects.exclude(mailings__user=user).filter(
            post_category__in=user_category,
            post_date__gte=request_period
        ).distinct().order_by('-post_date')

        if len(news) > 0:

            # print('test 4: ', user.username, '||', news.values_list('post_title', flat=True))

            subject = f'Новые публикации в категории {user_cat_str}'
            text_content = f'Новые публикации в категории {user_cat_str}:\n'
            html_content = f'Новые публикации в категории {user_cat_str}:<br>'
            n = 0
            for p in news:
                n += 1
                category_str = '|'.join(p.post_category.all().values_list('category_name', flat=True))
                text_content += (
                    f'{n}) {p.get_post_type_display()} - '
                    f'{p.post_title} '
                    f'({category_str}) - '
                    f'http://127.0.0.1:8000{p.get_absolute_url()}\n'
                )
                html_content += (
                    f'{n}) {p.get_post_type_display()} - '
                    f'<a href="http://127.0.0.1:8000{p.get_absolute_url()}">{p.post_title}</a> '
                    f'({category_str})<br>'
                )
                Mailing.objects.create(user=user, post=p)

            msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            # Для тестирования каждые 10 секунд:
            # trigger=CronTrigger(second="*/10"),
            # Статьи отправляются подписчикам каждую пятницу в 18:00:
            trigger=CronTrigger(minute="0", hour="18", day_of_week="fri"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

# Generated by Django 4.2.2 on 2023-08-06 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_remove_subscriber_last_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailings', to='news.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

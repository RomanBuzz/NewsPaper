# Generated by Django 4.2.2 on 2023-08-06 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_subscriber_last_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='last_sent',
        ),
    ]

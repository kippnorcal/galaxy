# Generated by Django 2.2.2 on 2019-07-01 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='resolution',
        ),
    ]

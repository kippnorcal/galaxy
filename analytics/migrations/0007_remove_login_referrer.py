# Generated by Django 2.2.4 on 2019-08-08 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_remove_login_resolution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='referrer',
        ),
    ]

# Generated by Django 2.2.4 on 2019-09-12 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_schoollevel_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='role_type',
            field=models.CharField(choices=[('S', 'staff'), ('L', 'leadership')], default='S', max_length=5),
        ),
    ]

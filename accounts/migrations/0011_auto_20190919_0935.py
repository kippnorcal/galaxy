# Generated by Django 2.2.5 on 2019-09-19 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_role_permission_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='permission_group',
            new_name='permission_groups',
        ),
    ]

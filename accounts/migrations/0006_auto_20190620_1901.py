# Generated by Django 2.2.2 on 2019-06-20 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='is_school',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='site',
            name='school_level',
            field=models.CharField(blank=True, choices=[('ES', 'ES'), ('MS', 'MS'), ('K8', 'K8'), ('HS', 'HS')], max_length=2, null=True),
        ),
    ]

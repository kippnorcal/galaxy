# Generated by Django 2.2.4 on 2019-08-11 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_publicstat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ('category', 'id'), 'verbose_name_plural': 'subcategories'},
        ),
        migrations.AddField(
            model_name='report',
            name='height',
            field=models.IntegerField(default=850),
        ),
    ]
# Generated by Django 2.2.4 on 2019-09-06 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('high_health', '0012_auto_20190905_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measure',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
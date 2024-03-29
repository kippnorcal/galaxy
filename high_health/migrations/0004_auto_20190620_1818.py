# Generated by Django 2.2.2 on 2019-06-20 18:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('high_health', '0003_auto_20190620_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metric',
            name='modified',
        ),
        migrations.AddField(
            model_name='metric',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='goal',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='measure',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='measure',
            name='goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='high_health.Goal'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='essential_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='high_health.EssentialQuestion'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Report'),
        ),
        migrations.AlterField(
            model_name='school',
            name='school_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='high_health.SchoolLevel'),
        ),
        migrations.AlterField(
            model_name='school',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Site'),
        ),
    ]

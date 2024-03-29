# Generated by Django 2.2.3 on 2019-07-29 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_schoollevel_display_name'),
        ('high_health', '0008_measure_is_current'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_type', models.CharField(choices=[('ABOVE', 'above'), ('BELOW', 'below')], default='ABOVE', max_length=5)),
                ('frequency', models.CharField(choices=[('MoM', 'month over month'), ('YoY', 'year over year')], default='MoM', max_length=3)),
                ('target', models.DecimalField(decimal_places=2, default=100, max_digits=5)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='high_health.Metric')),
                ('school', models.ForeignKey(limit_choices_to={'is_school': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Site')),
            ],
            options={
                'ordering': ['metric', 'school__school_level', 'school'],
            },
        ),
        migrations.AddField(
            model_name='metric',
            name='goals',
            field=models.ManyToManyField(through='high_health.Goal', to='accounts.Site'),
        ),
    ]

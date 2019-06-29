# Generated by Django 2.2.2 on 2019-06-20 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('high_health', '0005_goal_growth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='school_level',
        ),
        migrations.RemoveField(
            model_name='school',
            name='site',
        ),
        migrations.RenameField(
            model_name='metric',
            old_name='description',
            new_name='definition',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='goal',
        ),
        migrations.AddField(
            model_name='metric',
            name='goal_type',
            field=models.CharField(choices=[('ABOVE', 'above'), ('BELOW', 'below')], default='ABOVE', max_length=5),
        ),
        migrations.AddField(
            model_name='metric',
            name='growth_goal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='metric',
            name='performance_goal',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=5),
        ),
        migrations.AlterField(
            model_name='measure',
            name='school',
            field=models.ForeignKey(limit_choices_to={'is_school': True}, on_delete=django.db.models.deletion.PROTECT, to='accounts.Site'),
        ),
        migrations.DeleteModel(
            name='Goal',
        ),
        migrations.DeleteModel(
            name='School',
        ),
        migrations.DeleteModel(
            name='SchoolLevel',
        ),
    ]
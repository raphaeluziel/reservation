# Generated by Django 4.1.1 on 2022-11-09 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_shift_finish_time_alter_shift_shift_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='shift_end_date',
        ),
        migrations.AlterField(
            model_name='shift',
            name='finish_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='shift',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]

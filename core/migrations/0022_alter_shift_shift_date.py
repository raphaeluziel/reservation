# Generated by Django 4.1.1 on 2022-11-09 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_shift_shift_start_date_shift_shift_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='shift_date',
            field=models.DateField(verbose_name='Shift Date'),
        ),
    ]

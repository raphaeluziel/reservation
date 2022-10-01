# Generated by Django 4.1.1 on 2022-10-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_employer_user_remove_nurse_user_nurse_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nurse',
            old_name='phone_number',
            new_name='phone',
        ),
        migrations.AlterField(
            model_name='nurse',
            name='experience',
            field=models.IntegerField(choices=[(0, '<5'), (1, '<10'), (2, '>=10')]),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='role',
            field=models.CharField(choices=[('Sh', 'RN'), ('Lh', 'PN'), ('HA', 'AS')], max_length=2),
        ),
    ]

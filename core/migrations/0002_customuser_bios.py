# Generated by Django 4.1.1 on 2022-11-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bios',
            field=models.CharField(max_length=250, null=True),
        ),
    ]

# Generated by Django 4.1.1 on 2022-10-20 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='bank_account_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
# Generated by Django 3.0.6 on 2020-05-18 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0017_remove_blogpost_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.TextField(unique=True),
        ),
    ]

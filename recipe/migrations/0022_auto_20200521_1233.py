# Generated by Django 3.0.6 on 2020-05-21 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0021_blogpost_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='show',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.0.6 on 2020-05-18 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_blogpost_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default='2000-01-03'),
            preserve_default=False,
        ),
    ]

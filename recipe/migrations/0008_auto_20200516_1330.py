# Generated by Django 3.0.6 on 2020-05-16 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_auto_20200516_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='descreption',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.TextField(unique=True),
        ),
    ]

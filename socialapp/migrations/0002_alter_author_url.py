# Generated by Django 3.2.8 on 2021-11-25 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.URLField(default='http://cmput404-team13-socialapp.herokuapp.com/api/author/', max_length=100),
        ),
    ]

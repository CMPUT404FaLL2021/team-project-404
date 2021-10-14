# Generated by Django 3.2.8 on 2021-10-14 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0005_post_friends_only'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='friends_only',
        ),
        migrations.AddField(
            model_name='post',
            name='unlisted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(default='PUBLIC', max_length=30),
        ),
    ]

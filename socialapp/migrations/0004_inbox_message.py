# Generated by Django 3.2.8 on 2021-10-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0003_auto_20211027_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='message',
            field=models.CharField(default='Friend Request', max_length=32),
        ),
    ]

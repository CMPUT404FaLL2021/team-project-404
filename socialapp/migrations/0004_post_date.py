# Generated by Django 3.2.8 on 2021-10-12 02:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0003_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
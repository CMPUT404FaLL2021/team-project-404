# Generated by Django 3.1.6 on 2021-10-26 16:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('displayName', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('followers', models.ManyToManyField(blank=True, to='socialapp.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(default='', max_length=140)),
                ('description', models.CharField(default='', max_length=140)),
                ('contentType', models.CharField(default='PLAIN', max_length=30)),
                ('content', models.CharField(max_length=140)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('visibility', models.CharField(default='PUBLIC', max_length=30)),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socialapp.author')),
                ('likes', models.ManyToManyField(blank=True, related_name='post_likes', to='socialapp.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('comment', models.CharField(max_length=140)),
                ('contentType', models.CharField(default='PLAIN', max_length=30)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialapp.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialapp.post')),
            ],
        ),
    ]

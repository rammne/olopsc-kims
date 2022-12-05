# Generated by Django 4.1.3 on 2022-11-19 21:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ownership',
            name='status',
        ),
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Accept'), (3, 'Decline')], default=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='student',
            field=models.ManyToManyField(related_name='items', through='base.Ownership', to=settings.AUTH_USER_MODEL),
        ),
    ]

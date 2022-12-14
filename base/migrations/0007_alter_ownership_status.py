# Generated by Django 4.1.3 on 2022-11-26 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_ownership_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownership',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Declined'), (4, 'Reverted')], default=1),
        ),
    ]

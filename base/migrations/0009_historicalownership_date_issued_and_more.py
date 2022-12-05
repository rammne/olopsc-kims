# Generated by Django 4.1.3 on 2022-11-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_ownership_date_issued_historicalownership'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalownership',
            name='date_issued',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='ownership',
            name='date_issued',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

# Generated by Django 3.1.3 on 2021-01-01 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20210101_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='status',
        ),
    ]

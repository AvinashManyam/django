# Generated by Django 3.1.3 on 2020-12-26 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20201226_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='location',
            field=models.CharField(default='india', max_length=30),
        ),
    ]

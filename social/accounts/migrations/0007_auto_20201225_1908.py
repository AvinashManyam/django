# Generated by Django 3.1.3 on 2020-12-25 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(default='India?Edit', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.CharField(default='Please Mention anything', max_length=100),
        ),
    ]

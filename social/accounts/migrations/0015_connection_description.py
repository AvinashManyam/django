# Generated by Django 3.1.3 on 2020-12-29 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20201228_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
    ]

# Generated by Django 3.1.3 on 2021-01-02 11:54

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_chat_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='message',
            field=multiselectfield.db.fields.MultiSelectField(default=None, max_length=200),
        ),
    ]

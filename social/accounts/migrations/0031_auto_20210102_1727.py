# Generated by Django 3.1.3 on 2021-01-02 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_connection_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connection',
            name='message',
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', multiselectfield.db.fields.MultiSelectField(default=None, max_length=200)),
                ('read', multiselectfield.db.fields.MultiSelectField(default=None, max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-30 05:55

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_connection_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='broker',
            name='work',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('1', 'monday'), ('2', 'tuesday'), ('3', 'wednesday'), ('4', 'thursday'), ('5', 'friday'), ('6', 'saturday'), ('7', 'sunday')], max_length=13),
        ),
    ]

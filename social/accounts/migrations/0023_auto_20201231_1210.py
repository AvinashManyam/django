# Generated by Django 3.1.3 on 2020-12-31 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_customer_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='avg_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customer',
            name='rated_cust',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='present_bro', to='accounts.broker')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='present_cust', to='accounts.customer')),
            ],
        ),
    ]

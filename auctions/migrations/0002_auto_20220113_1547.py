# Generated by Django 3.2.9 on 2022-01-13 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='auction',
        ),
        migrations.AddField(
            model_name='category',
            name='auction',
            field=models.ManyToManyField(related_name='categories', to='auctions.Auction'),
        ),
    ]

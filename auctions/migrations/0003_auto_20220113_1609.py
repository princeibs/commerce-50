# Generated by Django 3.2.9 on 2022-01-13 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20220113_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='auction',
        ),
        migrations.AddField(
            model_name='category',
            name='auction',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction'),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.2.9 on 2022-01-13 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20220113_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='auction',
            field=models.ForeignKey(default='Others', on_delete=django.db.models.deletion.CASCADE, to='auctions.auction'),
        ),
    ]

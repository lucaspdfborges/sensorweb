# Generated by Django 2.0.9 on 2018-12-10 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesq', '0019_auto_20181210_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimento',
            name='last_data',
            field=models.FloatField(),
        ),
    ]

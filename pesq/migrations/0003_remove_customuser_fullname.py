# Generated by Django 2.0.9 on 2018-10-25 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pesq', '0002_auto_20181025_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='fullname',
        ),
    ]

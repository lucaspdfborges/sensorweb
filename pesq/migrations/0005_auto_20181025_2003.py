# Generated by Django 2.0.9 on 2018-10-25 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pesq', '0004_auto_20181025_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pesquisador',
            old_name='user',
            new_name='usuario',
        ),
    ]

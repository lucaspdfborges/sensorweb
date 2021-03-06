# Generated by Django 2.0.9 on 2018-10-30 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pesq', '0009_auto_20181029_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_publicacao', models.DateField()),
                ('titulo', models.TextField()),
                ('revista', models.TextField()),
                ('link', models.URLField(blank=True)),
                ('campos', models.ManyToManyField(to='pesq.Linhas')),
                ('pesquisador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 2.2.4 on 2019-08-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_auto_20190805_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='game_status',
            field=models.CharField(default='ready', max_length=200, null=True),
        ),
    ]
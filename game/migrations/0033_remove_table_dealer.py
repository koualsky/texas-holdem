# Generated by Django 2.2.4 on 2019-08-07 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0032_auto_20190806_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='dealer',
        ),
    ]

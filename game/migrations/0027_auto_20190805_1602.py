# Generated by Django 2.2.4 on 2019-08-05 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_auto_20190805_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='table',
            field=models.IntegerField(null=True),
        ),
    ]

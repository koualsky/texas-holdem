# Generated by Django 2.2.4 on 2019-08-04 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20190803_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='cards_on_table',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='dealer',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='deck',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='players',
            field=models.CharField(max_length=500, null=True),
        ),
    ]

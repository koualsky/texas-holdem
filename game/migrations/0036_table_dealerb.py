# Generated by Django 2.2.4 on 2019-08-07 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0035_remove_table_dealerr'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='dealerb',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dealerb', to='game.Player'),
        ),
    ]
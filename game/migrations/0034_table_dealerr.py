# Generated by Django 2.2.4 on 2019-08-07 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0033_remove_table_dealer'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='dealerr',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dealer', to='game.Player'),
        ),
    ]
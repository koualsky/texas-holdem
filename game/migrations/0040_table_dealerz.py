# Generated by Django 2.2.4 on 2019-08-08 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0039_remove_table_dealerzz'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='dealerz',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dealer', to='game.Player'),
        ),
    ]

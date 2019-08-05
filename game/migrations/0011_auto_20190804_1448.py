# Generated by Django 2.2.4 on 2019-08-04 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20190804_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='player1',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='game.Player'),
        ),
        migrations.AlterField(
            model_name='table',
            name='player2',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='game.Player'),
        ),
        migrations.AlterField(
            model_name='table',
            name='player3',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player3', to='game.Player'),
        ),
        migrations.AlterField(
            model_name='table',
            name='player4',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player4', to='game.Player'),
        ),
    ]

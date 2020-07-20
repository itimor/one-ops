# Generated by Django 3.0.3 on 2020-07-20 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0004_auto_20200720_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chats.ChatGroup', verbose_name='群组'),
        ),
    ]

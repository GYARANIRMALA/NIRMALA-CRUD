# Generated by Django 4.0.5 on 2022-09-13 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1_app', '0023_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=8),
        ),
    ]

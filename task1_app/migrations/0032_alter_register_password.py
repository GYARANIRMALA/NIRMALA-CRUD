# Generated by Django 4.0.5 on 2022-09-14 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1_app', '0031_alter_user_created_by_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=255),
        ),
    ]
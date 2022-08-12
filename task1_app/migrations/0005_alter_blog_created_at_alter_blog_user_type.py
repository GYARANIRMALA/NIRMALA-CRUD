# Generated by Django 4.0.5 on 2022-08-09 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1_app', '0004_blog_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='user_type',
            field=models.CharField(default='', max_length=15),
        ),
    ]

# Generated by Django 4.0.5 on 2022-08-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1_app', '0008_alter_blog_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='active',
            field=models.BooleanField(),
        ),
    ]
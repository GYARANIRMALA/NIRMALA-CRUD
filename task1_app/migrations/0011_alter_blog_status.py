# Generated by Django 4.0.5 on 2022-08-12 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1_app', '0010_alter_blog_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('pending', 'Pending')], default='', max_length=50),
        ),
    ]

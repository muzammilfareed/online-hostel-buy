# Generated by Django 2.0.7 on 2023-01-01 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20221231_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='house_info',
            name='name',
            field=models.TextField(default=''),
        ),
    ]

# Generated by Django 2.0.7 on 2022-12-31 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house_info',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]

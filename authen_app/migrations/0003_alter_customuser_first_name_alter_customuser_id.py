# Generated by Django 4.1.3 on 2023-01-02 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authen_app', '0002_auto_20221231_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

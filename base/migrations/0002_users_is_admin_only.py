# Generated by Django 4.0.2 on 2022-02-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_admin_only',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 3.0.2 on 2020-01-27 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_user_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

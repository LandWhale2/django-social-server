# Generated by Django 3.0.2 on 2020-02-12 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_chattinglist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.DecimalField(decimal_places=4, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.DecimalField(decimal_places=4, max_digits=7, null=True),
        ),
    ]
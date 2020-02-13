# Generated by Django 3.0.2 on 2020-02-12 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_auto_20200212_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=10, null=True),
        ),
    ]
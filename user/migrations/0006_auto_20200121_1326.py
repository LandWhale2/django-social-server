# Generated by Django 3.0.2 on 2020-01-21 04:26

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200120_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.user_path),
        ),
    ]

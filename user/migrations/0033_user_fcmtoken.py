# Generated by Django 3.0.2 on 2020-02-13 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0032_auto_20200213_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fcmtoken',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

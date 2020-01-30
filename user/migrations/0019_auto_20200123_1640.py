# Generated by Django 3.0.2 on 2020-01-23 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_remove_test_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TEST',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userhate',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userlike',
        ),
        migrations.AlterField(
            model_name='relation',
            name='relation_type',
            field=models.CharField(blank=True, choices=[('l', '좋아요'), ('b', '차단'), ('h', '싫어요')], max_length=1),
        ),
    ]
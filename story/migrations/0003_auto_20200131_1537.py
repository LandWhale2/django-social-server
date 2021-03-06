# Generated by Django 3.0.2 on 2020-01-31 06:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_user_age'),
        ('story', '0002_testmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryAlarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('nickname', models.CharField(max_length=20)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='storyalarm', to='user.User')),
            ],
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
    ]

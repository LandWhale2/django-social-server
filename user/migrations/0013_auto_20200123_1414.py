# Generated by Django 3.0.2 on 2020-01-23 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20200123_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('f', '팔로잉'), ('b', '차단')], max_length=1)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_by_from_user', to='user.User')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_by_to_user', to='user.User')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='relations',
            field=models.ManyToManyField(related_name='_user_relations_+', through='user.Relation', to='user.User'),
        ),
    ]

# Generated by Django 2.2.4 on 2019-09-07 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clienti',
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.IntegerField()),
                ('arrabbiato', models.IntegerField(default=0)),
                ('felice', models.IntegerField(default=0)),
                ('triste', models.IntegerField(default=0)),
                ('disgustato', models.IntegerField(default=0)),
                ('sorpreso', models.IntegerField(default=0)),
                ('annoiato', models.IntegerField(default=0)),
                ('impaurito', models.IntegerField(default=0)),
                ('sequence', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Statistiche',
                'verbose_name_plural': 'Statistiche',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='static/video/')),
                ('poster', models.FileField(upload_to='static/poster/')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Video',
            },
        ),
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.IntegerField()),
                ('titleV', models.CharField(max_length=100)),
                ('response', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=100)),
                ('sequence', models.IntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Client')),
            ],
            options={
                'verbose_name': 'Emozione',
                'verbose_name_plural': 'Emozioni',
            },
        ),
    ]

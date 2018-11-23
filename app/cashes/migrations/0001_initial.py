# Generated by Django 2.1.3 on 2018-11-23 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hammer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=20)),
                ('amount', models.IntegerField()),
                ('use_or_save', models.CharField(choices=[('u', 'use'), ('s', 'save')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HappyCash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=20)),
                ('amount', models.IntegerField()),
                ('use_or_save', models.CharField(choices=[('u', 'use'), ('s', 'save')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

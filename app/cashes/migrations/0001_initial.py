# Generated by Django 2.1.4 on 2018-12-20 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_uid', models.CharField(max_length=100)),
                ('amount', models.PositiveIntegerField()),
                ('hammer_or_cash', models.CharField(choices=[('hc', 'HappyCash'), ('hm', 'Hammer')], max_length=3)),
                ('use_or_save', models.CharField(choices=[('u', 'use'), ('s', 'save')], max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('purchased', models.BooleanField(default=False)),
            ],
        ),
    ]

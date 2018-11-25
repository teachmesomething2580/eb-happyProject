# Generated by Django 2.1.3 on 2018-11-25 05:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cashes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='happycash',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='happycash_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hammer',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hammer_user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]

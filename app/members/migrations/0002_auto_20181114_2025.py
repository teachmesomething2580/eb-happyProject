# Generated by Django 2.1.3 on 2018-11-14 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('use_point', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='online_available_use_category_limit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='use_point.Category'),
        ),
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Rating'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
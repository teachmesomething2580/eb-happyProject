# Generated by Django 2.1.3 on 2018-11-27 09:57

from django.db import migrations, models
import django.db.models.deletion
import giftcard.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCardCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('shop_image', models.ImageField(blank=True, null=True, upload_to='images/shop_image')),
            ],
        ),
        migrations.CreateModel(
            name='GiftCardType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gift_card_unique_id', models.CharField(default=giftcard.models.increment_giftcard_cnt, editable=False, max_length=8)),
                ('amount', models.IntegerField()),
                ('is_hotdeal', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('h', 'hot'), ('m', 'mobile')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='OrderGiftCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='OrderGiftCardAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('gift_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftcard.GiftCardType')),
            ],
        ),
        migrations.CreateModel(
            name='PINGiftCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PIN', models.CharField(max_length=30)),
                ('is_used', models.BooleanField(default=True)),
                ('created_in_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftcard.OrderGiftCardAmount')),
            ],
        ),
        migrations.CreateModel(
            name='AddressOrderGiftCard',
            fields=[
                ('ordergiftcard_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='giftcard.OrderGiftCard')),
            ],
            bases=('giftcard.ordergiftcard',),
        ),
        migrations.CreateModel(
            name='EmailOrderGiftCard',
            fields=[
                ('ordergiftcard_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='giftcard.OrderGiftCard')),
                ('email', models.EmailField(max_length=254)),
            ],
            bases=('giftcard.ordergiftcard',),
        ),
        migrations.CreateModel(
            name='SMSOrderGiftCard',
            fields=[
                ('ordergiftcard_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='giftcard.OrderGiftCard')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
            ],
            bases=('giftcard.ordergiftcard',),
        ),
        migrations.AddField(
            model_name='ordergiftcardamount',
            name='order_gift_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giftcard.OrderGiftCard'),
        ),
    ]
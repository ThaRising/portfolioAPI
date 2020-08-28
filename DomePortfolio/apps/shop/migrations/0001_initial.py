# Generated by Django 3.1 on 2020-08-28 06:40

import DomePortfolio.lib.storage.gcp_storage
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import imagekit.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(storage=DomePortfolio.lib.storage.gcp_storage.ImageStorage(), upload_to='')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar')], default='EUR', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='EUR', max_digits=19)),
                ('sale', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('description', models.TextField()),
                ('download', models.FileField(storage=DomePortfolio.lib.storage.gcp_storage.FileStorage(), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('completed', models.BooleanField(default=False)),
                ('related_paypal_order', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('ordered_on', models.DateTimeField(null=True)),
                ('customer_email', models.EmailField(max_length=254, null=True)),
                ('customer_id', models.CharField(max_length=100, null=True)),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar')], default='EUR', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='EUR', max_digits=19)),
                ('purchased_with_sale', models.PositiveSmallIntegerField(default=0)),
                ('product_downloads_remaining', models.PositiveSmallIntegerField(null=True)),
                ('download_expires_on', models.DateTimeField(null=True)),
                ('product_download', models.URLField(null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='shop.item')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_field', models.PositiveSmallIntegerField(default=0)),
                ('image', imagekit.models.fields.ProcessedImageField(storage=DomePortfolio.lib.storage.gcp_storage.ImageStorage(), upload_to='')),
                ('image_after', imagekit.models.fields.ProcessedImageField(storage=DomePortfolio.lib.storage.gcp_storage.ImageStorage(), upload_to='')),
                ('parent_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.item')),
            ],
            options={
                'ordering': ['order_field'],
                'abstract': False,
            },
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-06 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0004_product_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Electronics', 'Electronics'), ('Fashion and Beauty', 'Fashion and Beauty'), ('Home and Garden', 'Home and Garden'), ('Sports and Leisure', 'Sports and Leisure')], default='Electronics', max_length=50),
        ),
    ]

# Generated by Django 3.1.4 on 2020-12-04 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
    ]

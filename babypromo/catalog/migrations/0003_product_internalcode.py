# Generated by Django 2.2 on 2019-04-18 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20190417_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='internalCode',
            field=models.CharField(default=None, max_length=20),
        ),
    ]

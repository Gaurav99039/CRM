# Generated by Django 5.1.5 on 2025-01-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_order_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='note',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]

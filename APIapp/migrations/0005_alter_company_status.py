# Generated by Django 4.0.1 on 2022-01-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIapp', '0004_alter_transaction_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.CharField(choices=[('1', 'active'), ('0', 'inactive')], default='active', max_length=20),
        ),
    ]
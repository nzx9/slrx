# Generated by Django 3.2.5 on 2021-08-23 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0004_auto_20210823_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='verified',
            field=models.BooleanField(null=True),
        ),
    ]

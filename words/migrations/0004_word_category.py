# Generated by Django 3.2.5 on 2021-10-30 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('words', '0003_auto_20210804_0531'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.category'),
        ),
    ]
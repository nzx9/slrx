# Generated by Django 3.2.5 on 2021-08-23 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('streams', '0003_rename_user_streams_user_stream'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='comment',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='verified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]

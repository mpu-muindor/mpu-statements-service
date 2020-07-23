# Generated by Django 3.0.8 on 2020-07-23 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests_teachers', '0003_auto_20200721_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestteacher',
            name='contacts',
            field=models.CharField(default='фио', max_length=1000, verbose_name='Контактные данные'),
        ),
        migrations.AddField(
            model_name='requestteacher',
            name='user_uuid',
            field=models.UUIDField(default='91e265f1-9ed7-4c7a-add4-a0bd01562a4b', verbose_name='UUID пользователя'),
        ),
    ]

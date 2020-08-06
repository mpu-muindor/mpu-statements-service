# Generated by Django 3.0.8 on 2020-07-23 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests_students', '0003_requeststudent_contacts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requeststudent',
            name='contacts',
            field=models.CharField(max_length=1000, verbose_name='Контактные данные'),
        ),
        migrations.AlterField(
            model_name='requeststudent',
            name='user_uuid',
            field=models.UUIDField(verbose_name='UUID пользователя'),
        ),
    ]
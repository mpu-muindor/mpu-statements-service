# Generated by Django 3.0.8 on 2020-07-17 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1500, verbose_name='Структурное подразделение, адрес')),
            ],
        ),
        migrations.CreateModel(
            name='RequestType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1500, verbose_name='Запрос')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата, время')),
                ('reg_number', models.CharField(max_length=13, verbose_name='Рег. номер')),
                ('request_text', models.CharField(max_length=5000, verbose_name='Текст запроса')),
                ('status', models.SmallIntegerField(choices=[(1, 'На рассмотрении'), (2, 'Отклонена'), (3, 'Готово')], default=1, verbose_name='Статус')),
                ('date_for_status', models.DateTimeField(auto_now=True, verbose_name='Дата статуса')),
                ('remark', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Примечание')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requests.Address', verbose_name='Структурное подразделение, адрес')),
                ('request_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requests.RequestType', verbose_name='Запрос')),
            ],
            options={
                'verbose_name': 'Справки, заявления',
                'verbose_name_plural': 'Справки, заявления',
                'ordering': ['datetime'],
            },
        ),
    ]

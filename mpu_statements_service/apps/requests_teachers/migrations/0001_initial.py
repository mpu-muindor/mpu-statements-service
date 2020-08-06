# Generated by Django 3.0.8 on 2020-07-21 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestTeacherType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1500, verbose_name='Запрос')),
            ],
            options={
                'verbose_name': 'вид запроса',
                'verbose_name_plural': 'виды запросов',
            },
        ),
        migrations.CreateModel(
            name='ResponsibleUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1500, verbose_name='Название подразделения')),
            ],
            options={
                'verbose_name': 'Адрес подразделения',
                'verbose_name_plural': 'адреса подразделений',
            },
        ),
        migrations.CreateModel(
            name='RequestTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_text', models.CharField(max_length=5000, verbose_name='Текст заявки')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата, время')),
                ('request_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requests_teachers.RequestTeacherType', verbose_name='Тема заявки')),
                ('responsible_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requests_teachers.ResponsibleUnit', verbose_name='Ответственное подразделение')),
            ],
            options={
                'verbose_name': 'Цифровые сервисы для преподавателей',
                'verbose_name_plural': 'Цифровые сервисы для преподавателей',
                'ordering': ['datetime'],
            },
        ),
    ]
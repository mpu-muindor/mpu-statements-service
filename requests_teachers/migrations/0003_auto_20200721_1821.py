# Generated by Django 3.0.8 on 2020-07-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests_teachers', '0002_auto_20200721_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestteacher',
            name='request_title',
            field=models.SmallIntegerField(choices=[(1, 'Получение нового компьютерного оборудования'), (2, 'Подключение компьютера, МФУ, телефона, WiFi'), (3, 'Обслуживание принтеров, МФУ'), (4, 'Вопрос по СЭД Directum и 1С'), (5, 'Вопрос по Личному кабинету'), (6, 'Прочее ИТ-обслуживание'), (7, 'Справка с места работы'), (8, 'Справка на визу'), (9, 'Справка о стаже работы'), (10, 'Справка о количестве неиспользованных дней отпуска'), (11, 'Копия трудовой книжки'), (12, 'Копии документов из личного дела'), (13, 'Справка о работе на условиях внешнего совместительства для внесения стажа в трудовую книжку'), (14, 'Справка по форме 2-НДФЛ'), (15, 'Справка о выплате (не выплате) единовременного пособия на рождение ребенка'), (16, 'Справка об отпуске по уходу за ребенком до 1,5 и 3 лет'), (17, 'Справка о ежемесячных выплатах сотрудника, находящегося в отпуске по уходу за ребенком (декрет)')], verbose_name='Тема'),
        ),
        migrations.AlterField(
            model_name='requestteacher',
            name='responsible_unit',
            field=models.SmallIntegerField(choices=[(1, 'Отдел кадров, вн.тел 1130'), (2, 'Диспетчерская УИТ, вн.тел 1111')], verbose_name='Ответственное подразделение'),
        ),
    ]
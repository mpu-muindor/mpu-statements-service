from django.db import models


class ResponsibleUnit(models.Model):
    """
    Таблица ответственных подразделений
    """
    name = models.CharField(verbose_name="Название подразделения", max_length=1500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адрес подразделения"
        verbose_name_plural = "адреса подразделений"


class RequestTeacherType(models.Model):
    """
    Виды справок для преподавателей
    """
    name = models.CharField(verbose_name="Запрос", max_length=1500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "вид запроса"
        verbose_name_plural = "виды запросов"


class RequestTeacher(models.Model):
    """
    Цифровые сервисы (запросы) для преподавателей
    """
    REQUESTS = (
        (1, "Получение нового компьютерного оборудования"),
        (2, "Подключение компьютера, МФУ, телефона, WiFi"),
        (3, "Обслуживание принтеров, МФУ"),
        (4, "Вопрос по СЭД Directum и 1С"),
        (5, "Вопрос по Личному кабинету"),
        (6, "Прочее ИТ-обслуживание"),
        (7, "Справка с места работы"),
        (8, "Справка на визу"),
        (9, "Справка о стаже работы"),
        (10, "Справка о количестве неиспользованных дней отпуска"),
        (11, "Копия трудовой книжки"),
        (12, "Копии документов из личного дела"),
        (13, "Справка о работе на условиях внешнего совместительства для внесения стажа в трудовую книжку"),
        (14, "Справка по форме 2-НДФЛ"),
        (15, "Справка о выплате (не выплате) единовременного пособия на рождение ребенка"),
        (16, "Справка об отпуске по уходу за ребенком до 1,5 и 3 лет"),
        (17, "Справка о ежемесячных выплатах сотрудника, находящегося в отпуске по уходу за ребенком (декрет)"),
    )
    UNITS = (
        (1, "Отдел кадров, вн.тел 1130"),
        (2, "Диспетчерская УИТ, вн.тел 1111"),
    )
    ADDRESSES = (
        (1, "Б. Семёновская, д. 38"),
        (2, "1-я Дубровская, д. 16а"),
        (3, "Павла Корчагина, д. 22"),
        (4, "Автозаводская, д. 16"),
        (5, "Лефортовский вал, д. 26"),
        (6, "Прянишникова, д. 2А"),
        (7, "Садово-Спасская, д. 6"),
        (8, "Михалковская, д. 7"),
    )
    request_title = models.SmallIntegerField(choices=REQUESTS, verbose_name="Тема")
    request_text = models.CharField(verbose_name="Текст заявки", max_length=5000)
    responsible_unit = models.SmallIntegerField(choices=UNITS, verbose_name="Ответственное подразделение")
    datetime = models.DateTimeField(verbose_name="Дата, время", auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(
            self.request_title, self.responsible_unit, self.datetime
        )

    class Meta:
        verbose_name = "Цифровые сервисы для преподавателей"
        verbose_name_plural = verbose_name
        ordering = ["datetime"]

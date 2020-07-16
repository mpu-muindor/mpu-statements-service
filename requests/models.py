from django.db import models


class Request(models.Model):
    """
    Класс запросов (справки, заявки) пользователя
    """
    status_approved = 1
    status_rejected = 2
    status_done = 3
    STATUSES = (
        (status_approved, "На рассмотрении"),
        (status_rejected, "Отклонена"),
        (status_done, "Готово"),
    )

    address_bs = 1
    address_av = 2
    address_av2 = 3
    address_pr = 4
    address_pk = 5
    address_pr2 = 6
    address_ss = 7
    ADDRESSES = (
        (address_bs, "Отделение «На Большой Семеновской» центра по работе со студентами "
                     "Ул. Большая Семеновская, 38; ауд. В-107. "
                     "Тел. (495) 223-05-23 (доб. 1375, 1215, 1105) ; crs-bs@mospolytech.ru"),
        (address_av, "Отделение «На Автозаводской» центра по работе со студентами "
                     "Ул. Автозаводская, 16, ауд. 2315. Тел. (495) 276-33-30 доб. 2285"),
        (address_av2, "Отделение «На Автозаводской» центра по работе со студентами "
                      "ул. Автозаводская, 16, ауд. 2315. "
                      "Тел. (495) 276-37-30 доб. 2256, 2257,2285; crs-av@mospolytech.ru"),
        (address_pr, "Отделение «На Прянишникова» центра по работе со студентами "
                     "Ул. Михалковская, 7, ауд. 3307. "
                     "Тел. (495) 223-05-23 доб. 4059, 4060, 4061; crs-mikhalka@mospolytech.ru"),
        (address_pk, "Отделение «На Павла Корчагина» центра по работе со студентами "
                     "Ул. Павла Корчагина, 22, ауд. 213. "
                     "Тел. (495) 223-05-23 доб. 3043, 3044, 3045; crs-pk@mospolytech.ru"),
        (address_pr2, "Отделение «На Прянишникова» центра по работе со студентами "
                      "ул. Прянишникова, 2а, ауд. 1311. "
                      "Тел. (495) 223-05-23 доб. 4052, 4056, 4057; crs-pryaniki@mospolytech.ru"),
        (address_ss, "Отделение «На Садовой-Спасской» центра по работе со студентами "
                     "ул. Садовая-Спасская, 6, ауд. 4107, 4108. "
                     "Тел. (495) 223-05-23 доб. 4068, 4069, 4070; crs-sady@mospolytech.ru"),
    )

    REQUESTS = (
        # Центры по работе со студентами
        (1, "Справка о прослушанных дисциплинах за период обучения (справка об обучении)"),
        (2, "Справка о прохождении обучения в университете (о статусе обучающегося) по месту требования"),
        (3, "Справка в социальные учреждения (Пенсионный фонд, УСЗН и пр.)"),
        (4, "Справка-вызов"),
        (5, "Запрос на изменение персональных данных"),
        (6, "Запрос на восстановление магнитного пропуска"),
        # Практика
        (7, "Записаться на практику"),
        (8, "Заказать сопроводительное письмо на практику"),
        # Отдел платных образовательных услуг
        (9, "Оформить дополнительное соглашение к договору об обучении"),
        (10, "Отправить квитанцию об оплате обучения или пени"),
        # Профсоюзная организация
        (11, "Оформить дотацию Мэрии г. Москвы"),
        (12, "Заявка на материальную помощь"),
        (13, "Оформить социальную стипендию"),
        # Мобилизационный отдел
        (14, "Справка для получения отсрочки от призыва на военную службу"),
        # Прочее
        (15, "Произвольный запрос"),
    )
    # TODO: add user info (name, group, phone, email, etc...)
    datetime = models.DateTimeField(verbose_name="Дата, время", auto_now_add=True)
    reg_number = models.CharField(verbose_name="Рег. номер", max_length=13)
    request_title = models.SmallIntegerField(verbose_name="Запрос", choices=REQUESTS)
    request_text = models.CharField(verbose_name="Текст запроса", max_length=1000)
    status = models.SmallIntegerField(verbose_name="Статус", choices=STATUSES, default=status_approved)
    date_for_status = models.DateTimeField(verbose_name="Дата статуса", auto_now=True)
    address = models.SmallIntegerField(choices=ADDRESSES, verbose_name="Структурное подразделение, адрес",
                                       default=address_bs)
    remark = models.CharField(verbose_name="Примечание", max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{} {} {}".format(
            self.reg_number, self.request_text, self.status
        )

    class Meta:
        verbose_name = "Справки, заявления"
        verbose_name_plural = verbose_name
        ordering = ["datetime"]


class EducationRequest(models.Model):
    # phone =
    # email =
    DOC_TYPE = (
        (1, "аттестат о среднем (полном) общем образовании"),
        (2, "диплом о среднем профессиональном образовании"),
        (3, "диплом о начальном профессиональном образовании"),
        (4, "академическая справка или диплом о неполном высшем образовании"),
        (5, "диплом о полном высшем образовании"),
    )
    radio1 = models.BooleanField(blank=True, null=True)
    radio2 = models.BooleanField(blank=True, null=True)
    university_out = models.CharField(verbose_name="Наименование вуза на момент отчисления",
                                      max_length=300, blank=True, null=True)
    year_out = models.IntegerField(verbose_name="в году",
                                   blank=True, null=True)
    previous_doc_year = models.IntegerField(verbose_name="в году")
    doc = models.SmallIntegerField(choices=DOC_TYPE, verbose_name="Предыдущий документ об образовании")
    university_in = models.CharField(verbose_name="Наименование вуза на момент зачисления", max_length=300)
    year_in = models.IntegerField(verbose_name="в году")
    user_comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def to_text(self):
        temp = 'моим письменным заявлением.' if self.radio1 else f'отчислением из {self.university_out} в {self.year_out} году.'
        text = f'''
Прошу выдать мне справку об обучении в связи с {temp} Предыдущий документ об образовании, 
выданный в {self.previous_doc_year}: {dict(self.DOC_TYPE).get(self.doc)}. 
В {self.university_in} зачислен(а) в {self.year_in} году.'''.replace('\n', '')
        return text

from django.db import models


class Address(models.Model):
    """
    Модель адресов корпусов университета
    """
    name = models.CharField(verbose_name="Структурное подразделение, адрес", max_length=1500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "адрес"
        verbose_name_plural = "адреса"


class RequestType(models.Model):
    """
    Виды справок (Об обучении, в ПРФ, об отсрочке и т.д.)
    """
    name = models.CharField(verbose_name="Запрос", max_length=1500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "вид справки"
        verbose_name_plural = "виды справок"


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

    # address_bs = 1
    # address_av = 2
    # address_av2 = 3
    # address_pr = 4
    # address_pk = 5
    # address_pr2 = 6
    # address_ss = 7
    # ADDRESSES = (
    #     (address_bs, "Отделение «На Большой Семеновской» центра по работе со студентами "
    #                  "Ул. Большая Семеновская, 38; ауд. В-107. "
    #                  "Тел. (495) 223-05-23 (доб. 1375, 1215, 1105) ; crs-bs@mospolytech.ru"),
    #     (address_av, "Отделение «На Автозаводской» центра по работе со студентами "
    #                  "Ул. Автозаводская, 16, ауд. 2315. Тел. (495) 276-33-30 доб. 2285"),
    #     (address_av2, "Отделение «На Автозаводской» центра по работе со студентами "
    #                   "ул. Автозаводская, 16, ауд. 2315. "
    #                   "Тел. (495) 276-37-30 доб. 2256, 2257,2285; crs-av@mospolytech.ru"),
    #     (address_pr, "Отделение «На Прянишникова» центра по работе со студентами "
    #                  "Ул. Михалковская, 7, ауд. 3307. "
    #                  "Тел. (495) 223-05-23 доб. 4059, 4060, 4061; crs-mikhalka@mospolytech.ru"),
    #     (address_pk, "Отделение «На Павла Корчагина» центра по работе со студентами "
    #                  "Ул. Павла Корчагина, 22, ауд. 213. "
    #                  "Тел. (495) 223-05-23 доб. 3043, 3044, 3045; crs-pk@mospolytech.ru"),
    #     (address_pr2, "Отделение «На Прянишникова» центра по работе со студентами "
    #                   "ул. Прянишникова, 2а, ауд. 1311. "
    #                   "Тел. (495) 223-05-23 доб. 4052, 4056, 4057; crs-pryaniki@mospolytech.ru"),
    #     (address_ss, "Отделение «На Садовой-Спасской» центра по работе со студентами "
    #                  "ул. Садовая-Спасская, 6, ауд. 4107, 4108. "
    #                  "Тел. (495) 223-05-23 доб. 4068, 4069, 4070; crs-sady@mospolytech.ru"),
    # )

    # REQUESTS = (
    #     # Центры по работе со студентами
    #     (1, "Справка о прослушанных дисциплинах за период обучения (справка об обучении)"),
    #     (2, "Справка о прохождении обучения в университете (о статусе обучающегося) по месту требования"),
    #     (3, "Справка в социальные учреждения (Пенсионный фонд, УСЗН и пр.)"),
    #     (4, "Справка-вызов"),
    #     (5, "Запрос на изменение персональных данных"),
    #     (6, "Запрос на восстановление магнитного пропуска"),
    #     # Практика
    #     (7, "Записаться на практику"),
    #     (8, "Заказать сопроводительное письмо на практику"),
    #     # Отдел платных образовательных услуг
    #     (9, "Оформить дополнительное соглашение к договору об обучении"),
    #     (10, "Отправить квитанцию об оплате обучения или пени"),
    #     # Профсоюзная организация
    #     (11, "Оформить дотацию Мэрии г. Москвы"),
    #     (12, "Заявка на материальную помощь"),
    #     (13, "Оформить социальную стипендию"),
    #     # Мобилизационный отдел
    #     (14, "Справка для получения отсрочки от призыва на военную службу"),
    #     # Прочее
    #     (15, "Произвольный запрос"),
    # )

    # TODO: add user info (name, group, phone, email, etc...)
    datetime = models.DateTimeField(verbose_name="Дата, время", auto_now_add=True)
    reg_number = models.CharField(verbose_name="Рег. номер", max_length=13)
    request_title = models.ForeignKey(RequestType, on_delete=models.CASCADE, verbose_name="Запрос")
    request_text = models.CharField(verbose_name="Текст запроса", max_length=5000)
    status = models.SmallIntegerField(verbose_name="Статус", choices=STATUSES, default=status_approved)
    date_for_status = models.DateTimeField(verbose_name="Дата статуса", auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Структурное подразделение, адрес")
    remark = models.CharField(verbose_name="Примечание", max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{} {} {}".format(
            self.reg_number, self.request_title.name, self.status
        )

    class Meta:
        verbose_name = "Справки, заявления"
        verbose_name_plural = verbose_name
        ordering = ["datetime"]

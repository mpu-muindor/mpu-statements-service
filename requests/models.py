from django.db import models


class Address(models.Model):
    """
    Модель адресов корпусов университета
    """
    name = models.CharField(verbose_name="Структурное подразделение, адрес", max_length=1500)

    def __str__(self):
        return self.name[:50] + '...'

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
        (status_rejected, "Отклонено"),
        (status_done, "Готово"),
    )

    # TODO: add user info (name, group, phone, email, etc...)
    datetime = models.DateTimeField(verbose_name="Дата, время", auto_now_add=True)
    reg_number = models.CharField(verbose_name="Рег. номер", max_length=13)
    request_title = models.ForeignKey(RequestType, on_delete=models.CASCADE, verbose_name="Запрос")
    request_text = models.CharField(verbose_name="Текст запроса", max_length=5000)
    status = models.SmallIntegerField(verbose_name="Статус", choices=STATUSES, default=status_approved)
    date_for_status = models.DateTimeField(verbose_name="Дата статуса", auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Структурное подразделение, адрес")
    remark = models.CharField(verbose_name="Примечание", max_length=1000, blank=True, null=True)
    # TODO: add user comments and images from docs

    def __str__(self):
        return "{} {} {}".format(
            self.reg_number, self.request_title.name, self.status
        )

    class Meta:
        verbose_name = "Справки, заявления"
        verbose_name_plural = verbose_name
        ordering = ["datetime"]

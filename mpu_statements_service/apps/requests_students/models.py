from django.db import models


class Address(models.Model):
    """
    Модель адресов корпусов университета
    """
    name = models.CharField(verbose_name="Структурное подразделение, адрес", max_length=1500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адрес корпусов"
        verbose_name_plural = "адреса"


class RequestStudentType(models.Model):
    """
    Виды справок (Об обучении, в ПРФ, об отсрочке и т.д.)
    """
    name = models.CharField(verbose_name="Запрос", max_length=1500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "вид справки"
        verbose_name_plural = "виды справок"


class RequestStudent(models.Model):
    """
    Класс запросов (справки, заявки) студента
    """
    status_approved = 1
    status_rejected = 2
    status_done = 3
    STATUSES = (
        (status_approved, "На рассмотрении"),
        (status_rejected, "Отклонено"),
        (status_done, "Готово"))
    user_uuid = models.UUIDField(verbose_name='UUID пользователя')
    contacts = models.CharField(max_length=1000, verbose_name='Контактные данные')
    datetime = models.DateTimeField(verbose_name="Дата, время", auto_now_add=True)
    reg_number = models.CharField(verbose_name="Рег. номер", max_length=13)
    request_title = models.ForeignKey(RequestStudentType, on_delete=models.CASCADE, verbose_name="Запрос")
    request_text = models.CharField(verbose_name="Текст запроса", max_length=5000)
    status = models.SmallIntegerField(verbose_name="Статус", choices=STATUSES, default=status_approved)
    date_for_status = models.DateTimeField(verbose_name="Дата статуса", auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Структурное подразделение, адрес")
    remark = models.CharField(verbose_name="Примечание", max_length=1000, blank=True, null=True)
    docs = models.FileField(verbose_name="Файлы", upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    # TODO: add user comments and images from docs

    def get_addr(self):
        return self.address.name

    def __str__(self):
        return "{} {} {}".format(
            self.reg_number, self.request_title.name, self.status)

    class Meta:
        verbose_name = "Справки, заявления для студентов"
        verbose_name_plural = verbose_name
        ordering = ["datetime"]

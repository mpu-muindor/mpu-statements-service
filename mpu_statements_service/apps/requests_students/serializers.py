from django.db.utils import OperationalError
from rest_framework import serializers
from .models import Address, RequestStudentType, RequestStudent


def create_addresses():
    """Создание списка всех адресов университета"""
    addresses = [
        "Отделение «На Большой Семеновской» центра по работе со студентами Ул. Большая Семеновская, 38; ауд. В-107. Тел. (495) 223-05-23 (доб. 1375, 1215, 1105) ; crs-bs@mospolytech.ru",
        "Отделение «На Автозаводской» центра по работе со студентами Ул. Автозаводская, 16, ауд. 2315. Тел. (495) 276-33-30 доб. 2285",
        "Отделение «На Автозаводской» центра по работе со студентами ул. Автозаводская, 16, ауд. 2315. Тел. (495) 276-37-30 доб. 2256, 2257,2285; crs-av@mospolytech.ru",
        "Отделение «На Прянишникова» центра по работе со студентами Ул. Михалковская, 7, ауд. 3307. Тел. (495) 223-05-23 доб. 4059, 4060, 4061; crs-mikhalka@mospolytech.ru",
        "Отделение «На Павла Корчагина» центра по работе со студентами Ул. Павла Корчагина, 22, ауд. 213. Тел. (495) 223-05-23 доб. 3043, 3044, 3045; crs-pk@mospolytech.ru",
        "Отделение «На Прянишникова» центра по работе со студентами ул. Прянишникова, 2а, ауд. 1311. Тел. (495) 223-05-23 доб. 4052, 4056, 4057; crs-pryaniki@mospolytech.ru",
        "Отделение «На Садовой-Спасской» центра по работе со студентами ул. Садовая-Спасская, 6, ауд. 4107, 4108. Тел. (495) 223-05-23 доб. 4068, 4069, 4070; crs-sady@mospolytech.ru",

        "Договорной отдел Москва, Большая Семеновская, д. 38, ауд. Н-402, тел. (495) 223-05-40, (495) 223-05-23 доб. 1247, 1549, 1550",
        "Мобилизационный отдел г. Москва, ул. Б. Семёновская, д. 38, корп. А, кабинеты А-324, 325. Тел.: (495) 223-05-23, доб. 1225",
        "Отдел практики и трудоустройства 107023, г. Москва, ул. Б. Семёновская, д. 38, корпус «А», ауд. А - 319",
        "Профсоюзная организация работников и обучающихся 107023, г. Москва, ул. Б. Семеновская, д. 38, аудитория В-202. Тел. 495 223-05-31"
    ]
    for address in addresses:
        Address.objects.get_or_create(name=address)


try:
    create_addresses()
except OperationalError:
    pass


def get_addresses(filter_name=None):
    """
    Получить список всех адресов
    """
    if filter_name:
        try:
            addresses = list(Address.objects.filter(name__contains=filter_name))
        except OperationalError:
            addresses = list()
    else:
        try:
            addresses = list(Address.objects.all())
        except OperationalError:
            addresses = list()
    choices = tuple(
        (a.id, a.name) for a in addresses
    )
    return choices


def get_request_type_and_num(request_name):
    """
    Получить тип справки и соответствующий регистрационный номер
    :param request_name: Название типа справки
    """
    obj, _ = RequestStudentType.objects.get_or_create(name=request_name)

    try:
        num = RequestStudent.objects.filter(request_title__name=request_name).last().id + 1
    except AttributeError:
        num = 1

    return obj, num


def get_default_address(name=None):
    """
    Получить дефолтный адрес выдачи справок
    """
    if name:
        obj, _ = Address.objects.get_or_create(name=name)
    else:
        # Подразумевается ЦРС На Большой Семёновской
        obj, _ = Address.objects.get_or_create(
            name="Отделение «На Большой Семеновской» центра по работе со "
                 "студентами Ул. Большая Семеновская, 38; ауд. В-107. Тел. (495) "
                 "223-05-23 (доб. 1375, 1215, 1105) ; crs-bs@mospolytech.ru"
        )
    return obj


def get_contacts(user, validated_data):
    contacts = f'{user.name}, {validated_data.get("phone", user.phone)},' \
               f' {validated_data.get("email", user.email)}'
    return user, contacts


class BaseSerializerStudent(serializers.Serializer):
    """
    Базовай класс сериалайзера, содержащий поля phone, email, user_comment,
    котоые есть во всех справках
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    user_comment = serializers.CharField(required=False, allow_null=True)

    def save(self, **kwargs):
        self.user, self.contacts = get_contacts(self.context['user'], self.validated_data)


class EdRequestSerializerStudent(BaseSerializerStudent):
    """
    Справка о прослушанных дисциплинах за период обучения (справка об обучении)
    """
    radio1 = serializers.NullBooleanField(required=False)
    radio2 = serializers.NullBooleanField(required=False)
    university_out = serializers.CharField(required=False, allow_null=True)
    year_out = serializers.CharField(required=False, allow_null=True)
    previous_doc_year = serializers.CharField()

    DOC_TYPE = (
        (1, "аттестат о среднем (полном) общем образовании"),
        (2, "диплом о среднем профессиональном образовании"),
        (3, "диплом о начальном профессиональном образовании"),
        (4, "академическая справка или диплом о неполном высшем образовании"),
        (5, "диплом о полном высшем образовании"))
    previous_doc = serializers.ChoiceField(choices=DOC_TYPE)
    university_in = serializers.CharField()
    year_in = serializers.CharField()

    def save(self, **kwargs):
        # Retrieve user
        super(EdRequestSerializerStudent, self).save()
        group_id = '171-371'

        # Request text formatting
        temp = 'моим письменным заявлением.' \
            if self.validated_data["radio1"] else f'отчислением из {self.validated_data["university_out"]} в ' \
                                                  f'{self.validated_data["year_out"]} году.'
        text = f'Прошу выдать мне справку об обучении в связи с {temp} Предыдущий документ об образовании, ' + \
               f'выданный в {self.validated_data["previous_doc_year"]} году: ' \
               f'{dict(self.DOC_TYPE).get(self.validated_data["previous_doc"])}. ' + \
               f'В {self.validated_data["university_in"]} зачислен(а) в {self.validated_data["year_in"]} году. ' \
               f'Учебная группа: {group_id}.'
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'

        # Get request title
        request_name = "Справка о прослушанных дисциплинах за период обучения (справка об обучении)"
        obj, num = get_request_type_and_num(request_name)

        # Create request
        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"ED{num}",
            request_title=obj,
            request_text=text,
            address=get_default_address())


class StatusRequestSerializerStudent(BaseSerializerStudent):
    """
    Справка о прохождении обучения в университете (о статусе обучающегося) по месту требования
    """
    address = serializers.ChoiceField(choices=get_addresses("центра по работе со студентами"))
    to_whom = serializers.CharField(max_length=500)

    def save(self, **kwargs):
        super(StatusRequestSerializerStudent, self).save()

        text = f'Дана для предоставления {self.validated_data["to_whom"]}.'
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'

        request_name = "Справка о прохождении обучения в университете (о статусе обучающегося) по месту требования"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"SR{num}",
            request_title=obj,
            request_text=text,
            address=Address.objects.get(pk=self.validated_data["address"]))


class SobesRequestSerializerStudent(BaseSerializerStudent):
    """
    Справка в социальные учреждения (Пенсионный фонд, УСЗН и пр.)
    """
    address = serializers.ChoiceField(choices=get_addresses("центра по работе со студентами"))
    order_num = serializers.CharField()
    order_date = serializers.CharField()
    to_whom = serializers.CharField(max_length=500)

    def save(self, **kwargs):
        super(SobesRequestSerializerStudent, self).save()

        text = f'Зачислена(а) по приказу от {self.validated_data["order_date"]} {self.validated_data["order_num"]}. ' + \
               f'Дана для предоставления {self.validated_data["to_whom"]}.'
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'

        request_name = "Справка в социальные учреждения (Пенсионный фонд, УСЗН и пр.)"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"SC{num}",
            request_title=obj,
            request_text=text,
            address=Address.objects.get(pk=self.validated_data["address"]))


class CallRequestSerializerStudent(BaseSerializerStudent):
    """
    Справка-вызов
    """
    date_from = serializers.DateField(format="%d.%m.%Y")
    date_to = serializers.DateField(format="%d.%m.%Y")

    def save(self, **kwargs):
        super(CallRequestSerializerStudent, self).save()

        date_from = self.validated_data["date_from"].strftime("%d.%m.%Y")
        date_to = self.validated_data["date_to"].strftime("%d.%m.%Y")
        day_delta = (self.validated_data["date_to"] - self.validated_data["date_from"]).days
        text = f'Период гарантий с: {date_from} по: {date_to}. Кол-во дней: {day_delta}.'
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'

        request_name = "Справка-вызов"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"SPV{num}",
            request_title=obj,
            request_text=text,
            address=get_default_address())


class PersDataRequestSerializerStudent(BaseSerializerStudent):
    """
    Запрос на изменение персональных данных
    """
    first_last_name = serializers.CharField(max_length=500)
    reason = serializers.CharField(max_length=500)
    docs = serializers.FileField()

    def save(self, **kwargs):
        super(PersDataRequestSerializerStudent, self).save()

        text = f'Прошу внести изменения в мои персональные данные и в дальнейшем именовать меня ' + \
               f'{self.validated_data["first_last_name"]} в связи с {self.validated_data["reason"]}'

        request_name = "Запрос на изменение персональных данных"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"PD{num}",
            request_title=obj,
            request_text=text,
            address=get_default_address())


class PassRestoreRequestSerializerStudent(BaseSerializerStudent):
    """
    Запрос на восстановление магнитного пропуска
    """
    reason = serializers.CharField(max_length=500)

    def save(self, **kwargs):
        super(PassRestoreRequestSerializerStudent, self).save()

        text = f'Прошу восстановить мой магнитный пропуск в связи с {self.validated_data["reason"]}'

        request_name = "Запрос на восстановление магнитного пропуска"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"RP{num}",
            request_title=obj,
            request_text=text,
            address=get_default_address())


class PracticeSelectRequestSerializerStudent(BaseSerializerStudent):
    """
    Выбор места практики
    """
    pass


class PracticeLetterRequestSerializerStudent(BaseSerializerStudent):
    """
    Заказ сопроводительного письма на прохождение практики
    """
    PRACTICE_TYPES = (
        (1, "учебная"),
        (2, "производственная"),
        (3, "преддипломная"),
        (4, "другое"))
    another_practice = serializers.CharField(required=False, allow_null=True)
    practice_type = serializers.ChoiceField(choices=PRACTICE_TYPES)
    date_from = serializers.DateField(format="%d.%m.%Y")
    date_to = serializers.DateField(format="%d.%m.%Y")
    organization_name = serializers.CharField(max_length=300)
    organization_head = serializers.CharField(max_length=300)

    def save(self, **kwargs):
        super(PracticeLetterRequestSerializerStudent, self).save()

        group_id = '171-371'
        phone = self.validated_data.get("phone", self.user.phone)
        email = self.validated_data.get("email", self.user.email)

        date_from = self.validated_data["date_from"].strftime("%d.%m.%Y")
        date_to = self.validated_data["date_to"].strftime("%d.%m.%Y")
        # TODO: не хватает специальности и нормальной группы
        text = f'{self.user.name},\nГруппа: {group_id},\nПериод: с {date_from} до {date_to},\n' + \
               f'Место практики: {self.validated_data["organization_name"]},\n' + \
               f'Руководитель: {self.validated_data["organization_head"]},\n' \
               f'Специальность: 09.03.03 Прикладная информатика,\n' \
               f'Тел: {phone},\nE-mail: {email}'

        request_name = "Заказать сопроводительное письмо на практику"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"PRL{num}",
            request_title=obj,
            request_text=text,
            address=get_default_address(
                name="Отдел практики и трудоустройства 107023, г. Москва, ул. Б. Семёновская, "
                     "д. 38, корпус «А», ауд. А - 319"
            ))


class ExtraAgreementRequestSerializerStudent(BaseSerializerStudent):
    """
    Заключение дополнительного соглашения к договору об обучении
    """
    pass


class SendPaymentEduRequestSerializerStudent(BaseSerializerStudent):
    """
    Отправка квитанции об оплате за обучение, неустойку (пени)
    """
    pass


class MatHelpRequestSerializerStudent(BaseSerializerStudent):
    """
    Заявка на оказание материальной помощи
    """
    department = serializers.CharField(max_length=700)
    REASONS = (
        (1, "Нуждающиеся в дорогостоящем лечении и (или) восстановлении здоровья, в том числе в компенсации расходов "
            "на операцию, приобретение дорогостоящих медикаментов при наличии соответствующих медицинских "
            "рекомендаций, проведении необходимых платных медицинских осмотров и обследований, профилактических "
            "прививок"),
        (2, "Дети-сироты и дети, оставшиеся без попечения родителей"),
        (3, "Лица из числа детей-сирот и детей, оставшихся без попечения родителей"),
        (4, "Потерявшие в период обучения обоих или единственного родителя"),
        (5, "Признанные в установленном порядке инвалидами I, II группы, инвалидами с детства (вне зависимости от "
            "установленной группы инвалидности)"),
        (6, "Дети-инвалиды"),
        (7, "Инвалиды и ветераны боевых действий"),
        (8, "Пострадавшие в результате аварии на Чернобыльской АЭС и других радиационных катастроф"),
        (9, "Обучающиеся, признанные в установленном порядке инвалидами III группы (за исключением инвалидов III "
            "группы – инвалидов с детства)"),
        (10, "Обучающиеся из малоимущих семей или одиноко проживающие обучающиеся, среднедушевой доход которых ниже "
             "величины прожиточного минимума, установленного в соответствующем субъекте РФ и (или) получившие "
             "государственную социальную помощь"),
        (11, "Обучающиеся, имеющие обоих родителей (единственного родителя), являющихся инвалидом и (или) пенсионером"),
        (12, "Обучающиеся, потерявшие во время обучения в университете одного из родителей (потеря кормильца)"),
        (13, "Обучающиеся из неполных семей"),
        (14, "Обучающиеся из многодетных семей"),
        (15, "В связи с бракосочетанием"),
        (16, "Обучающиеся женского пола, вставшим на учет в медицинском учреждении по беременности"),
        (17, "В связи с рождением ребенка"),
        (18, "Обучающиеся, являющиеся одинокой матерью (отцом)"),
        (19, "Обучающиеся, имеющие на иждивении ребенка (детей)"),
        (20, "Семьи обучающихся с ребенком (детьми)"),
        (21, "В связи со смертью близкого родственника (супруг (супруга), ребенок (дети), мать, отец, брат и/или "
             "сестра (полнородные и неполнородные), бабушка, дедушка)"),
        (22, "Обучающиеся, пострадавшие при чрезвычайных обстоятельствах (стихийных бедствиях, техногенных авариях, "
             "вооруженных конфликтах, экологических катастрофах, пожарах, несчастных случаях)"),
        (23, "В целях компенсации расходов на проезд от места постоянного жительства к месту учебы и обратно"),
        (24, "В целях компенсации расходов в связи с мотивированной необходимостью улучшения жилищных условий"),
        (25, "Временно оказавшиеся в сложной жизненной ситуации, в иных ситуациях по решению Комиссии"),
        (26, "Обучающиеся, имеющие право на получение государственной социальной стипендии в условиях предупреждения "
             "распространения новой коронавирусной инфекции COVID-19 на территории РФ"),
        (27, "Обучающиеся, проживающие в общежитиях Московского Политеха в условиях реализации мероприятий по "
             "предотвращению распространения коронавирусной инфекции COVID-19"))
    reason = serializers.MultipleChoiceField(choices=REASONS)
    docs = serializers.FileField()

    def save(self, **kwargs):
        choises = {
            1: "с тем, что я нуждаюсь в дорогостоящем лечении и (или) восстановлении здоровья",
            2: "с тем, что я являюсь сиротой или оставшим(ей)ся без попечения родителей",
            3: "с тем, что я являюсь сиротой или оставшим(ей)ся без попечения родителей",
            4: "с тем, что я являюсь потерявшим(ей) в период обучения обоих или единственного родителя",
            5: "с тем, что я признан(а) в установленном порядке инвалидами I, II группы, инвалидами с детства",
            6: "с тем, что я являюсь ребенком-инвалидом",
            7: "с тем, что я являюсь инвалидом и ветераном боевых действий",
            8: "с тем, что я являюсь пострадавшим(ей) в результате аварии на Чернобыльской АЭС и других радиационных катастроф",
            9: "с тем, что я являюсь обучающимся и признан(а) в установленном порядке инвалидом III группы",
            10: "с тем, что я являюсь обучающимся из малоимущих семей или одиноко проживающим, среднедушевой доход которых ниже величины прожиточного минимума, установленного в соответствующем субъекте РФ и (или) получивший государственную социальную помощь",
            11: "с тем, что я являюсь обучающимся, имеющим обоих родителей (единственного родителя), являющихся инвалидом и (или) пенсионером",
            12: "с тем, что я являюсь обучающимся, потерявшим во время обучения в университете одного из родителей (потеря кормильца)",
            13: "с тем, что я являюсь обучающимся из неполных семей",
            14: "с тем, что я являюсь обучающимся из многодетных семей",
            15: "с бракосочетанием",
            16: "с тем, что я являюсь обучающимся женского пола, вставшей на учет в медицинском учреждении по беременности",
            17: "с рождением ребенка",
            18: "с тем, что я являюсь обучающимся, являющимся одинокой матерью (отцом)",
            19: "с тем, что я являюсь обучающимся, имеющим на иждивении ребенка (детей)",
            20: "с тем, что я являюсь представителем семьи обучающихся с ребенком",
            21: "со смертью близкого родственника",
            22: "с тем, что я являюсь обучающимся, пострадавшим при чрезвычайных обстоятельствах",
            23: "с необходимостью компенсации расходов на проезд от места постоянного жительства к месту учебы и обратно",
            24: "с необходимостью компенсации расходов в связи с мотивированной необходимостью улучшения жилищных условий",
            25: "с тем, что я оказался(ась)в сложной жизненной ситуации",
            26: "с тем, что я имею право на получение государственной социальной стипендии в условиях предупреждения распространения новой коронавирусной инфекции COVID-19 на территории РФ",
            27: "с тем, что я являюсь обучающимся, проживающим в общежитиях Московского Политеха в условиях реализации мероприятий по предотвращению распространения коронавирусной инфекции COVID-19",
        }
        temp_reasons = list(dict(self.REASONS).get(key) for key in self.validated_data["reason"])
        text = f'Основания: {", ".join(temp_reasons)}.\n' \
               f'Прошу оказать мне материальную помощь '

        temp_reasons = list(choises.get(key) for key in self.validated_data["reason"])
        reasons = ', а также '.join(temp_reasons)
        text += reasons + '.\n'

        super(MatHelpRequestSerializerStudent, self).save()
        group_id = '171-371'  # TODO: valid group
        phone = self.validated_data.get("phone", self.user.phone)

        text += f'Подразделение: {self.validated_data["department"]}\nКурс: 3\nГруппа: {group_id}\n' \
                f'Основа обучения: Бюджетная\nКатегория обучаещегося: студент\nКонтактный телефон: {phone}\n '

        request_name = "Заявка на материальную помощь"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"MR{num}",
            request_title=obj,
            request_text=text,
            address=get_default_address(
                name="Профсоюзная организация работников и обучающихся 107023, г. Москва, "
                     "ул. Б. Семеновская, д. 38, аудитория В-202. Тел. 495 223-05-31"
            ))


class SocStipRequestSerializerStudent(BaseSerializerStudent):
    """
    Оформление социальной стипендии
    """
    REASONS = (
        (1, "Являющиеся детьми-сиротами и детьми, оставшимися без попечения родителей, лицами из числа детей-сирот и "
            "детей, оставшихся без попечения родителей, лицами, потерявшими в период обучения обоих родителей или "
            "единственного родителя, детьми-инвалидами"),
        (2, "Являющиеся инвалидами I и II групп, инвалидами с детства"),
        (3, "Подвергшиеся воздействию радиации вследствие катастрофы на Чернобыльской АЭС и иных радиационных "
            "катастроф, вследствие ядерных испытаний на Семипалатинском полигоне"),
        (4, "Являющиеся инвалидами вследствие военной травмы или заболевания, полученных в период прохождения военной "
            "службы, и ветеранами боевых действий, а также студентам из числа граждан, проходивших в течение не менее "
            "трех лет военную службу по контракту на воинских должностях, подлежащих замещению солдатами, матросами, "
            "сержантами, старшинами, и уволенных с военной службы по основаниям, предусмотренным подпунктами «б» - "
            "«г» пункта 1, подпунктом «а» пункта 2 и подпунктами «а» - «в» пункта 3 статьи 51 Федерального закона от "
            "28 марта 1998 года N 53-ФЗ «О воинской обязанности и военной службе»"),
        (5, "Получившие государственную социальную помощь"))
    reason = serializers.ChoiceField(choices=REASONS)
    docs = serializers.FileField()

    def save(self, **kwargs):
        super(SocStipRequestSerializerStudent, self).save()

        text = f'Основание для получения социальнй стипендии: {dict(self.REASONS).get(self.validated_data["reason"])}.'

        request_name = "Оформить социальную стипендию"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"PS{num}",
            request_title=obj,
            request_text=text,
            address=get_default_address(
                name="Профсоюзная организация работников и обучающихся 107023, г. Москва, "
                     "ул. Б. Семеновская, д. 38, аудитория В-202. Тел. 495 223-05-31"))


class ForeignLanguageSerializerHelper(serializers.Serializer):
    language = serializers.CharField(max_length=20)
    proficiency = serializers.CharField(max_length=20)


class EducationSerializerHelper(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    diploma = serializers.CharField(max_length=20)
    year = serializers.CharField(max_length=10)
    qualification = serializers.CharField(max_length=50)
    specialty = serializers.CharField(max_length=50)


class FamilySerializerHelper(serializers.Serializer):
    relation_degree = serializers.CharField(max_length=30)
    fio = serializers.CharField(max_length=50)
    year = serializers.CharField(max_length=10)


class ArmyRequestSerializerStudent(BaseSerializerStudent):
    """
    Сервис пердназначен для постановки на воинский учет обучающихся - граждан,
    пребывающих в запасе (ГПЗ) и граждан, подлежащие призыву (ГПП).
    На основании заполненных данных вам будет оформлена справка (приложение №2),
    которая является основанием для предоставления отсрочки от призыва в Вооруженные Силы.
    """
    EDUCATIONS = (
        (1, "среднее общее"),
        (2, "среднее полное"),
        (3, "начальное профессиональное"),
        (4, "среднее профессиональное"),
        (5, "высшее профессиональное"))
    SUITABILITY_CATEGORIES = (
        (1, "А"),
        (2, "Б"),
        (3, "В"),
        (4, "Г"))
    MARTIAL_STATUSES = (
        (1, "холост"),
        (2, "женат"))
    RESERVE_CATEGORIES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
    )
    home_phone = serializers.CharField(max_length=18)  # Контактные данные
    birthplace = serializers.CharField(max_length=200)  # Место рождения
    inn = serializers.CharField(max_length=12)
    snils = serializers.CharField(max_length=11)
    citizenship = serializers.CharField(max_length=50)  # Гражданство
    # language_proficiency = ForeignLanguageSerializerHelper(many=True)  # Владение иностранными языками
    language = serializers.CharField(max_length=20)
    proficiency = serializers.CharField(max_length=20)
    education = serializers.ChoiceField(choices=EDUCATIONS)
    #
    # education_institutions = EducationSerializerHelper(many=True)  # образовательные учреждения
    name = serializers.CharField(max_length=50)
    diploma = serializers.CharField(max_length=20)
    end_year = serializers.CharField(max_length=10)
    qualification = serializers.CharField(max_length=50)
    specialty = serializers.CharField(max_length=50)
    #
    martial_status = serializers.ChoiceField(choices=MARTIAL_STATUSES)
    # family_members = FamilySerializerHelper(many=True)
    relation_degree = serializers.CharField(max_length=30)
    fio = serializers.CharField(max_length=50)
    fam_year = serializers.CharField(max_length=10)
    #
    user_address1 = serializers.CharField(max_length=200)  # Адрес места жительства по паспорту
    user_address2 = serializers.CharField(max_length=200)  # Адрес места жительства фактический
    registration_date = serializers.CharField(max_length=10)  # Дата регистрации по месту жительства
    # Паспортные данные
    pass_series = serializers.CharField(max_length=4)  # Серия паспорта
    pass_number = serializers.CharField(max_length=6)  # Номер паспорта
    issued = serializers.CharField(max_length=100)  # Кем выдано
    issue_date = serializers.CharField(max_length=10)  # Дата выдачи
    code = serializers.CharField(max_length=7)  # Код подраделения
    # Сведения о воинском учёте
    reserve_category = serializers.ChoiceField(RESERVE_CATEGORIES)  # Категория запаса
    military_rank = serializers.CharField(max_length=100)  # Воинское звание
    profile = serializers.CharField(max_length=100)  # Состав (профиль)
    vus_code = serializers.CharField(max_length=100)  # Полное кодовое обозначение ВУС
    suitability_category = serializers.ChoiceField(SUITABILITY_CATEGORIES)  # Категория годности
    commissariat_name = serializers.CharField(max_length=100)  # Наименование военного комиссариата по месту жительства
    docs = serializers.FileField(required=False, allow_null=True)

    def save(self, **kwargs):
        super(ArmyRequestSerializerStudent, self).save()

        phone = self.validated_data.get("phone", self.user.phone)
        email = self.validated_data.get("email", self.user.email)
        birthday = self.user.birthday

        text = \
            f'Контактные данные: \n' \
            f'Тел. моб.: {phone} E-mail: {email} \n' \
            f'Тел. дом.: {self.validated_data["home_phone"]} \n' \
            f'Дата рождения: {birthday} \n' \
            f'Место рождения: {self.validated_data["birthplace"]} \n' \
            f'ИНН: {self.validated_data["inn"]} \n' \
            f'СНИЛС: {self.validated_data["snils"]} \n' \
            f'Гражданство: {self.validated_data["citizenship"]} \n' \
            f'Владение иностранными языками: {self.validated_data["language"]} {self.validated_data["proficiency"]} {self.validated_data["education"]} \n' \
            f'Образование: {dict(self.EDUCATIONS).get(self.validated_data["education"])} \n' \
            f'Образовательные учреждения: {self.validated_data["name"]} {self.validated_data["diploma"]} {self.validated_data["end_year"]} {self.validated_data["qualification"]} {self.validated_data["specialty"]} \n' \
            f'Семейное положение: {dict(self.MARTIAL_STATUSES).get(self.validated_data["martial_status"])} \n' \
            f'Состав семьи: {self.validated_data["relation_degree"]} {self.validated_data["fio"]} {self.validated_data["fam_year"]} \n' \
            f'Адрес места жительства по паспорту: {self.validated_data["user_address1"]} \n' \
            f'Адрес места жительства фактический: {self.validated_data["user_address2"]} \n' \
            f'Дата регистрации по месту жительства: {self.validated_data["registration_date"]} \n' \
            f'Паспортные данные: \n' \
            f'Серия {self.validated_data["pass_series"]} Номер {self.validated_data["pass_number"]} \n' \
            f'Кем выдан: {self.validated_data["issued"]} \n' \
            f'Дата выдачи {self.validated_data["issue_date"]} Код подразделения {self.validated_data["code"]} \n' \
            f'СВЕДЕНИЯ О ВОИНСКОМ УЧЕТЕ \n' \
            f'Категория запаса: {dict(self.RESERVE_CATEGORIES).get(self.validated_data["reserve_category"])} \n' \
            f'Воинское звание: {self.validated_data["military_rank"]} \n' \
            f'Состав (профиль): {self.validated_data["profile"]} \n' \
            f'Полное кодовое обозначение ВУС: {self.validated_data["vus_code"]} \n' \
            f'Категория годности: {dict(self.SUITABILITY_CATEGORIES).get(self.validated_data["suitability_category"])} \n' \
            f'Наименование военного комиссариата по месту жительства: {self.validated_data["commissariat_name"]} \n'

        request_name = "Справка для получения отсрочки от призыва на военную службу"
        obj, num = get_request_type_and_num(request_name)

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            reg_number=f"VK{num}",
            request_title=obj,
            request_text=text,
            address=get_default_address(
                name="Мобилизационный отдел г. Москва, ул. Б. Семёновская, д. 38, корп. А, "
                     "кабинеты А-324, 325. Тел.: (495) 223-05-23, доб. 1225"))


class FreeRequestSerializerStudent(BaseSerializerStudent):
    """
    Произвольный запрос
    """
    address = serializers.ChoiceField(choices=get_addresses())
    title = serializers.CharField(max_length=500)
    text = serializers.CharField(max_length=500)
    docs = serializers.FileField(required=False, allow_null=True)

    def save(self, **kwargs):
        text = self.validated_data["text"]
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'

        request_name = "Произвольный запрос"
        obj, num = get_request_type_and_num(request_name)

        super(FreeRequestSerializerStudent, self).save()

        RequestStudent.objects.create(
            user_uuid=self.user.id,
            contacts=self.contacts,
            request_title=obj,
            request_text=text,
            address=Address.objects.get(pk=self.validated_data["address"]))


class RequestHistoryStudentSerializer(serializers.ModelSerializer):
    """
    История запросов справок пользователя
    """
    # Django Model.get_FOO_display
    request_title = serializers.SerializerMethodField(source="get_request_title")
    datetime = serializers.SerializerMethodField(source="get_formatted_datetime")
    status = serializers.CharField(source="get_status_display")
    address = serializers.CharField(source="get_addr")
    date_for_status = serializers.SerializerMethodField(source="get_date_for_status")

    def get_request_title(self, obj):
        return obj.request_title.name

    def get_date_for_status(self, obj):
        return obj.date_for_status.strftime("%d.%m.%Y %H:%M")

    def get_datetime(self, obj):
        return obj.datetime.strftime("%d.%m.%Y %H:%M")

    class Meta:
        model = RequestStudent
        fields = ("datetime", "reg_number", "request_title", "request_text",
                  "status", "date_for_status", "address", "remark")


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "name",)


class RequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStudentType
        fields = ("id", "name",)

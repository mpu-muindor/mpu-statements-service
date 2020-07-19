from django.db import OperationalError
from rest_framework import serializers
from requests.models import *


def get_addresses():
    try:
        addresses = list(Address.objects.all())
    except:
        addresses = list()
    choices = tuple(
        (a.id, a.name) for a in addresses
    )
    return choices


class EdRequestSerializer(serializers.Serializer):
    """
    Справка о прослушанных дисциплинах за период обучения (справка об обучении)
    """

    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
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
        (5, "диплом о полном высшем образовании"),
    )
    previous_doc = serializers.ChoiceField(choices=DOC_TYPE)
    university_in = serializers.CharField()
    year_in = serializers.CharField()
    user_comment = serializers.CharField(required=False, allow_null=True)

    def save(self, **kwargs):
        temp = 'моим письменным заявлением.' \
            if self.validated_data["radio1"] else f'отчислением из {self.validated_data["university_out"]} в ' \
                                                  f'{self.validated_data["year_out"]} году.'
        text = f'Прошу выдать мне справку об обучении в связи с {temp} Предыдущий документ об образовании, ' + \
               f'выданный в {self.validated_data["previous_doc_year"]}: {dict(self.DOC_TYPE).get(self.validated_data["previous_doc"])}. ' + \
               f'В {self.validated_data["university_in"]} зачислен(а) в {self.validated_data["year_in"]} году.'
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'

        try:
            num = Request.objects.filter(request_title__id=1).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"ED{num}",
            request_title=RequestType.objects.get(pk=1),
            request_text=text,
            address=Address.objects.get(pk=1),
        )


class StatusRequestSerializer(serializers.Serializer):
    """
    Справка о прохождении обучения в университете (о статусе обучающегося) по месту требования
    """

    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    address = serializers.ChoiceField(choices=get_addresses())
    to_whom = serializers.CharField(max_length=500)
    user_comment = serializers.CharField(required=False, allow_null=True)

    def save(self, **kwargs):
        text = f'Дана для предоставления {self.validated_data["to_whom"]}.'
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'
        try:
            num = Request.objects.filter(request_title__id=2).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"SR{num}",
            request_title=RequestType.objects.get(pk=2),
            request_text=text,
            address=Address.objects.get(pk=self.validated_data["address"]),
        )


class SobesRequestSerializer(serializers.Serializer):
    """
    Справка в социальные учреждения (Пенсионный фонд, УСЗН и пр.)
    """

    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    address = serializers.ChoiceField(choices=get_addresses())
    order_num = serializers.CharField()
    order_date = serializers.CharField()
    to_whom = serializers.CharField(max_length=500)
    user_comment = serializers.CharField(required=False, allow_null=True)

    def save(self, **kwargs):
        text = f'Зачислена(а) по приказу от {self.validated_data["order_date"]} {self.validated_data["order_num"]}. ' + \
               f'Дана для предоставления {self.validated_data["to_whom"]}.'
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'
        try:
            num = Request.objects.filter(request_title__id=3).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"SC{num}",
            request_title=RequestType.objects.get(pk=3),
            request_text=text,
            address=Address.objects.get(pk=self.validated_data["address"]),
        )


class CallRequestSerializer(serializers.Serializer):
    """
    Справка-вызов
    """

    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    date_from = serializers.DateField(format="%d.%m.%Y")
    date_to = serializers.DateField(format="%d.%m.%Y")
    user_comment = serializers.CharField(required=False, allow_null=True)

    def save(self, **kwargs):
        date_from = self.validated_data["date_from"].strftime("%d.%m.%Y")
        date_to = self.validated_data["date_to"].strftime("%d.%m.%Y")

        day_delta = (self.validated_data["date_to"] - self.validated_data["date_from"]).days
        text = f'Период гарантий с: {date_from} по: {date_to}. Кол-во дней: {day_delta}.'
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'
        try:
            num = Request.objects.filter(request_title__id=4).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"SPV{num}",
            request_title=RequestType.objects.get(pk=4),
            request_text=text,
            address=Address.objects.get(pk=1),
        )


class PersDataRequestSerializer(serializers.Serializer):
    """
    Запрос на изменение персональных данных
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    first_last_name = serializers.CharField(max_length=500)
    reason = serializers.CharField(max_length=500)
    docs = serializers.FileField()

    def save(self, **kwargs):
        text = f'Прошу внести изменения в мои персональные данные и в дальнейшем именовать меня ' + \
               f'{self.validated_data["first_last_name"]} в связи с {self.validated_data["reason"]}'
        try:
            num = Request.objects.filter(request_title__id=5).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"PD{num}",
            request_title=RequestType.objects.get(pk=5),
            request_text=text,
            address=Address.objects.get(pk=1),
        )


class PassRestoreRequestSerializer(serializers.Serializer):
    """
    Заявление на восстановление магнитного пропуска
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    reason = serializers.CharField(max_length=500)

    def save(self, **kwargs):
        text = f'Прошу восстановить мой магнитный пропуск в связи с {self.validated_data["reason"]}'
        try:
            num = Request.objects.filter(request_title__id=6).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"RP{num}",
            request_title=RequestType.objects.get(pk=6),
            request_text=text,
            address=Address.objects.get(pk=1),
        )


class PracticeSelectRequestSerializer(serializers.Serializer):
    """
    Выбор места практики
    """
    pass


class PracticeLetterRequestSerializer(serializers.Serializer):
    """
    Заказ сопроводительного письма на прохождение практики
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    PRACTICE_TYPES = (
        (1, "учебная"),
        (2, "производственная"),
        (3, "преддипломная"),
        (4, "другое"),
    )
    another_practice = serializers.CharField(required=False, allow_null=True)
    practice_type = serializers.ChoiceField(choices=PRACTICE_TYPES)
    date_from = serializers.DateField(format="%d.%m.%Y")
    date_to = serializers.DateField(format="%d.%m.%Y")
    organization_name = serializers.CharField(max_length=300)
    organization_head = serializers.CharField(max_length=300)

    def save(self, **kwargs):
        # TODO: add user!!!
        date_from = self.validated_data["date_from"].strftime("%d.%m.%Y")
        date_to = self.validated_data["date_to"].strftime("%d.%m.%Y")
        text = f'ФИО студента,Группа:,Период: с {date_from} до {date_to},' + \
               f'Место практики: {self.validated_data["organization_name"]},' + \
               f'Руководитель: {self.validated_data["organization_head"]},Специальность:,Тел:,E-mail:'
        try:
            num = Request.objects.filter(request_title__id=8).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"PRL{num}",
            request_title=RequestType.objects.get(pk=8),
            request_text=text,
            address=Address.objects.get(pk=1),  # Отдел практики и трудоустройства
        )


class ExtraAgreementRequestSerializer(serializers.Serializer):
    """
    Заключение дополнительного соглашения к договору об обучении
    """
    pass


class SendPaymentEduRequestSerializer(serializers.Serializer):
    """
    Отправка квитанции об оплате за обучение, неустойку (пени)
    """
    pass


class PrDonateRequestSerializer(serializers.Serializer):
    """
    Оформление дотации Мэрии г. Москвы
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    REASONS = (
        (1, "сироты или оставшиеся без попечения родителей"),
        (2, "инвалиды"),
        (3, "члены многодетной семьи"),
        (4, "имеющие на иждивении ребёнка"),
        (5, "участники военных действий"),
        (6, "пострадавшие в результате аварии на Чернобыльской АЭС и других радиационных катастроф"),
        (7, "родители — инвалиды, пенсионеры"),
        (8, "члены неполной семьи"),
        (9, "хроническое заболевание"),
    )
    year = serializers.CharField(max_length=4)
    reason = serializers.ChoiceField(choices=REASONS)
    prof_ticket = serializers.CharField(max_length=100)
    user_address = serializers.CharField(max_length=300)
    docs = serializers.FileField()

    def save(self, **kwargs):
        choice = {
            1: 'я являюсь сиротой / остался(ась) без попечения родителей',
            2: 'я являюсь инвалидом',
            3: 'я член многодетной семьи',
            4: 'я имею на иждивении ребёнка',
            5: 'я являюсь участником военных действий',
            6: 'я пострадал(а) в результате аварии на Чернобыльской АЭС и других радиационных катастроф',
            7: 'мои родители – инвалиды / пенсионеры',
            8: 'я являюсь членом неполной семьи',
            9: 'я имею хроническое заболевание',
        }.get(self.validated_data["reason"])
        text = f'Прошу назначить меня на получение материальной поддержки остронуждающимся студентам ' + \
               f'в {self.validated_data["year"]} году в связи с тем, что: {choice}. ' + \
               f'Номер членского профсоюзного билета: {self.validated_data["prof_ticket"]}. ' + \
               f'Адрес по месту регистрации: {self.validated_data["user_address"]}.'
        try:
            num = Request.objects.filter(request_title__id=11).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"DN{num}",
            request_title=RequestType.objects.get(pk=11),  # адрес профсоюза на БС
            request_text=text,
            address=Address.objects.get(pk=1),
        )


class MatHelpRequestSerializer(serializers.Serializer):
    """
    Заявка на оказание материальной помощи
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    department = serializers.CharField(max_length=700)
    # TODO: add text formatting to reasons
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
            "предотвращению распространения коронавирусной инфекции COVID-19"),
    )
    reason = serializers.MultipleChoiceField(choices=REASONS)
    docs = serializers.FileField()

    def save(self, **kwargs):
        text = f'Факультет (институт)/структурное подразделение: {self.validated_data["department"]}. ' + \
               f'Прошу оказать мне материальную помощь из средств стипендиального фонда университета ' + \
               f'в связи с тем, что я {dict(self.REASONS).get(list(self.validated_data["reason"])[0])}.'
        try:
            num = Request.objects.filter(request_title__id=12).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"MR{num}",
            request_title=RequestType.objects.get(pk=12),
            request_text=text,
            address=Address.objects.get(pk=1),
        )


class SocStipRequestSerializer(serializers.Serializer):
    """
    Оформление социальной стипендии
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
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
        (5, "Получившие государственную социальную помощь"),
    )
    reason = serializers.ChoiceField(choices=REASONS)
    docs = serializers.FileField()

    def save(self, **kwargs):
        text = f'Основание для получения социальнй стипендии: {dict(self.REASONS).get(self.validated_data["reason"])}.'
        try:
            num = Request.objects.filter(request_title__id=13).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"PS{num}",
            request_title=RequestType.objects.get(pk=13),
            request_text=text,
            address=Address.objects.get(pk=1),
        )


class ArmyRequestSerializer(serializers.Serializer):
    """
    Запрос на получение в мобилизационном отделе справки (Приложение № 2)
    для получения отсрочки от призыва на военную службу в военном комиссариате
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    FACULTIES = (
        (1, "Факультет информационных технологий"),
        (2, "Транспортный факультет"),
        (3, "Факультет машиностроения"),
        (4, "Факультет химической технологии и биотехнологии"),
        (5, "Факультет урбанистики и городского хозяйства"),
        (6, "Факультет базовых компетенций"),
        (7, "Инженерная школа (факультет)"),
        (8, "Факультет довузовской подготовки"),
        (9, "Факультет дополнительного образования"),
        (10, "Институт графики и искусства книги имени В. А. Фаворского"),
        (11, "Институт коммуникаций и медиабизнеса"),
        (12, "Институт издательского дела и журналистики"),
        (13, "Институт принтмедиа и информационных технологий"),
    )
    faculty = serializers.ChoiceField(choices=FACULTIES)
    CATEGORIES = (
        (1, "А"),
        (2, "Б"),
        (3, "В"),
        (4, "Г"),
    )
    category = serializers.ChoiceField(choices=CATEGORIES)
    MARTIAL_STATUSES = (
        (1, "холост"),
        (2, "женат"),
    )
    martial_status = serializers.ChoiceField(choices=MARTIAL_STATUSES)
    wife = serializers.CharField(required=False, allow_null=True)
    children = serializers.CharField(required=False, allow_null=True)
    user_address = serializers.CharField()
    user_temp_address = serializers.CharField(required=False, allow_null=True)

    def save(self, **kwargs):
        # TODO: add user!!! (2)
        text = f'ФИО\nФакультет: {dict(self.FACULTIES).get(self.validated_data["faculty"])}\nСпециальность:\nДР:\nТел:\n' \
               f'Категория годности:{dict(self.CATEGORIES).get(self.validated_data["category"])}\n' \
               f'Место жительства: {self.validated_data["user_address"] }\n' \
               f'Семейное положение: {dict(self.MARTIAL_STATUSES).get(self.validated_data["martial_status"])}\n'

        if self.validated_data.get("children"):
            text += f'ФИО детей, дата рождения: {self.validated_data["children"]}\n'
        if self.validated_data.get("wife"):
            text += f'Жена: {self.validated_data["wife"]}\n'
        if self.validated_data.get("user_temp_address"):
            text += f'Временная регистрация: {self.validated_data["user_temp_address"]}\n'
        try:
            num = Request.objects.filter(request_title__id=14).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"VK{num}",
            request_title=RequestType.objects.get(pk=14),
            request_text=text,
            address=Address.objects.get(pk=1),
        )


class FreeRequestSerializer(serializers.Serializer):
    """
    Произвольный запрос
    """
    phone = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    address = serializers.ChoiceField(choices=get_addresses())
    title = serializers.CharField(max_length=500)
    text = serializers.CharField(max_length=500)
    user_comment = serializers.CharField(required=False, allow_null=True)
    docs = serializers.FileField(required=False, allow_null=True)

    def save(self, **kwargs):
        text = self.validated_data["text"]
        if self.validated_data.get("user_comment"):
            text += f' Комментарий: {self.validated_data["user_comment"]}'
        try:
            num = Request.objects.filter(request_title__id=15).last().id + 1
        except AttributeError:
            num = 1
        Request.objects.create(
            reg_number=f"FF{num}",
            request_title=RequestType.objects.get(pk=15),
            request_text=text,
            address=Address.objects.get(pk=self.validated_data["address"]),
        )


class MainPageRequestSerializer(serializers.ModelSerializer):
    """
    История запросов справок пользователя
    """
    # Django Model.get_FOO_display
    datetime = serializers.SerializerMethodField(source="get_formatted_datetime")
    status = serializers.ChoiceField(Request.STATUSES)
    date_for_status = serializers.SerializerMethodField(source="get_date_for_status")

    def get_date_for_status(self, obj):
        return obj.date_for_status.strftime("%d.%m.%Y %H:%M")

    def get_datetime(self, obj):
        return obj.datetime.strftime("%d.%m.%Y %H:%M")

    class Meta:
        model = Request
        fields = ("datetime", "reg_number", "request_title", "request_text",
                  "status", "date_for_status", "address", "remark")


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "name", )


class RequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestType
        fields = ("id", "name", )

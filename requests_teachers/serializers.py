from rest_framework import serializers
from requests_teachers.models import RequestTeacher


class ISandComputersSerializer(serializers.Serializer):
    """
    Сериалайзер для следующих типов справок:
     - Получение нового компьютерного оборудования
     - Подключение компьютера, МФУ, телефона, WiFi
     - Обслуживание принтеров, МФУ
     - Вопрос по СЭД Directum и 1С
     - Вопрос по Личному кабинету
     - Прочее ИТ-обслуживание
    """
    structural_unit = serializers.CharField()
    email = serializers.EmailField()
    work_phone = serializers.CharField(required=False, allow_null=True)
    mobile_phone = serializers.CharField()
    work_address_corpus = serializers.ChoiceField(choices=RequestTeacher.ADDRESSES)
    work_address_room = serializers.CharField()
    request_title = serializers.ChoiceField(choices=RequestTeacher.REQUESTS)
    request_text = serializers.CharField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)

    def save(self, **kwargs):
        user = self.context['user']
        contacts = f'{user.name}, {self.validated_data.get("phone", user.phone)}, {self.validated_data.get("email", user.email)}'

        text = f"Подразделение: {self.validated_data['structural_unit']}\nДолжность: Преподаватель,\n" \
               f"Моб. телефон: {self.validated_data['mobile_phone']}\n" \
               f"Площадка: {dict(RequestTeacher.ADDRESSES).get(self.validated_data['work_address_corpus'])}\n" \
               f"Номер аудитории: {self.validated_data['work_address_room']}\n"
        if self.validated_data.get("request_text"):
            text += f'Заявка:\n{self.validated_data["request_text"]}'

        RequestTeacher.objects.create(
            user_uuid=user.id,
            contacts=contacts,
            request_title=self.validated_data['request_title'],
            request_text=text,
            responsible_unit=2,
        )


class WorkRequestsSerializer(serializers.Serializer):
    """
    Сериалайзер для следующих типов справок:
     - Справка с места работы
     - Справка на визу
     - Справка о стаже работы
     - Справка о количестве неиспользованных дней отпуска
     - Копия трудовой книжки
     - Копии документов из личного дела
     - Справка о работе на условиях внешнего совместительства для внесения стажа в трудовую книжку
     - Справка об отпуске по уходу за ребенком до 1,5 и 3 лет
    """
    structural_unit = serializers.CharField()
    email = serializers.EmailField()
    work_phone = serializers.CharField(required=False, allow_null=True)
    mobile_phone = serializers.CharField()
    work_address_corpus = serializers.ChoiceField(choices=RequestTeacher.ADDRESSES)
    work_address_room = serializers.CharField()
    request_title = serializers.ChoiceField(choices=RequestTeacher.REQUESTS)
    request_text = serializers.CharField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)
    WAYS_TO_GET = (
        (1, "на электронную почту"),
        (2, "получить в МФЦ/отделе")
    )
    way_to_get = serializers.ChoiceField(choices=WAYS_TO_GET)
    PLACES_TO_GET = (
        (1, "МФЦ Большая Семёновская, д. 38, аудитория В107"),
        (2, "МФЦ Прянишникова, д. 2А, аудитория 1311"),
        (3, "МФЦ Павла Корчагина, д. 22, аудитория 213"),
        (4, "МФЦ Автозаводская, д. 16, аудитория 2315"),
        (5, "Отдел кадров"),
        (6, "Бухгалтерия"),
    )
    place_to_get = serializers.ChoiceField(choices=PLACES_TO_GET, required=False)

    def validate(self, data):
        """
        Проверка получения места справки
        """
        if data['way_to_get'] == 2 and not data.get("place_to_get", None):
            raise serializers.ValidationError({"place_to_get": "необходимо выбрать место получения справки"})
        return data

    def save(self, **kwargs):
        user = self.context['user']
        contacts = f'{user.name}, {self.validated_data.get("phone", user.phone)}, {self.validated_data.get("email", user.email)}'

        text = f"Подразделение: {self.validated_data['structural_unit']}\nДолжность: Преподаватель,\n" \
               f"Моб. телефон: {self.validated_data['mobile_phone']}\n" \
               f"Площадка: {dict(RequestTeacher.ADDRESSES).get(self.validated_data['work_address_corpus'])}\n" \
               f"Номер аудитории: {self.validated_data['work_address_room']}\n"
        if self.validated_data.get("request_text"):
            text += f'Заявка:\n{self.validated_data["request_text"]}'
        if self.validated_data["way_to_get"] == 2 and self.validated_data.get("place_to_get"):
            temp_way = f'в {dict(self.PLACES_TO_GET).get(self.validated_data["place_to_get"])}'
        else:
            temp_way = f'на почту: {self.validated_data["email"]}'
        text += f'\nСпособ получения: {temp_way}'

        RequestTeacher.objects.create(
            user_uuid=user.id,
            contacts=contacts,
            request_title=self.validated_data['request_title'],
            request_text=text,
            responsible_unit=1,
        )


class WorkPaymentsSerializer(serializers.Serializer):
    """
    Сериалайзер для следующих типов справок:
     - Справка по форме 2-НДФЛ
     - Справка о выплате (не выплате) единовременного пособия на рождение ребенка
     - Справка о ежемесячных выплатах сотрудника, находящегося в отпуске по уходу за ребенком (декрет)
    """
    structural_unit = serializers.CharField()
    email = serializers.EmailField()
    work_phone = serializers.CharField(required=False, allow_null=True)
    mobile_phone = serializers.CharField()
    work_address_corpus = serializers.ChoiceField(choices=RequestTeacher.ADDRESSES)
    work_address_room = serializers.CharField()
    request_title = serializers.ChoiceField(choices=RequestTeacher.REQUESTS)
    request_period = serializers.IntegerField(min_value=2010, max_value=2020, required=False)
    copies_number = serializers.IntegerField(min_value=1, max_value=10, required=False)
    child_fio = serializers.CharField(max_length=300, required=False)
    child_date = serializers.DateField(required=False)
    request_text = serializers.CharField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)
    WAYS_TO_GET = (
        (1, "на электронную почту"),
        (2, "получить в МФЦ/отделе")
    )
    way_to_get = serializers.ChoiceField(choices=WAYS_TO_GET)
    PLACES_TO_GET = (
        (1, "МФЦ Большая Семёновская, д. 38, аудитория В107"),
        (2, "МФЦ Прянишникова, д. 2А, аудитория 1311"),
        (3, "МФЦ Павла Корчагина, д. 22, аудитория 213"),
        (4, "МФЦ Автозаводская, д. 16, аудитория 2315"),
        (5, "Отдел кадров"),
        (6, "Бухгалтерия"),
    )
    place_to_get = serializers.ChoiceField(choices=PLACES_TO_GET, required=False)

    def validate(self, data):
        """
        Проверка получения места справки
        """
        if dict(RequestTeacher.REQUESTS).get(data["request_title"]) == 'Справка по форме 2-НДФЛ' and \
                not data.get("copies_number", None):
            raise serializers.ValidationError({
                "copies_number": "необходимо указать количество копий справки (число от 1 до 10)",
            })

        if dict(RequestTeacher.REQUESTS).get(data["request_title"]) == 'Справка по форме 2-НДФЛ' and \
                not data.get("request_period", None):
            raise serializers.ValidationError({
                "request_period": "необходимо указать период справки"
            })
        if dict(RequestTeacher.REQUESTS).get(data["request_title"]) == \
                'Справка о ежемесячных выплатах сотрудника, находящегося в отпуске по уходу за ребенком (декрет)' and \
                not data.get("request_period", None):
            raise serializers.ValidationError({
                "request_period": "необходимо указать период справки"
            })

        if data['way_to_get'] == 2 and not data.get("place_to_get", None):
            raise serializers.ValidationError({"place_to_get": "необходимо выбрать место получения справки"})

        if dict(RequestTeacher.REQUESTS).get(data["request_title"]) == \
                'Справка о выплате (не выплате) единовременного пособия на рождение ребенка' \
                and not (data.get("child_fio", None) or data.get("child_date", None)):
            raise serializers.ValidationError({
                "child_fio": "необходимо указать ФИО ребёнка",
                "child_date": "необходимо указать дату рождения ребёнка",
            })
        return data

    def save(self, **kwargs):
        user = self.context['user']
        contacts = f'{user.name}, {self.validated_data.get("phone", user.phone)}, {self.validated_data.get("email", user.email)}'

        text = f"Подразделение: {self.validated_data['structural_unit']}\nДолжность: Преподаватель,\n" \
               f"Моб. телефон: {self.validated_data['mobile_phone']}\n" \
               f"Площадка: {dict(RequestTeacher.ADDRESSES).get(self.validated_data['work_address_corpus'])}\n" \
               f"Номер аудитории: {self.validated_data['work_address_room']}\n"
        if self.validated_data.get("request_text"):
            text += f'Заявка:\n{self.validated_data["request_text"]}'
        if self.validated_data["way_to_get"] == 2 and self.validated_data.get("place_to_get"):
            temp_way = f'в {dict(self.PLACES_TO_GET).get(self.validated_data["place_to_get"])}'
        else:
            temp_way = f'на почту: {self.validated_data["email"]}'
        text += f'\nСпособ получения: {temp_way}'
        if dict(RequestTeacher.REQUESTS).get(self.validated_data["request_title"]) == 'Справка по форме 2-НДФЛ':
            text += f'\nКоличество копий: {self.validated_data["copies_number"]}'

        RequestTeacher.objects.create(
            user_uuid=user.id,
            contacts=contacts,
            request_title=self.validated_data['request_title'],
            request_text=text,
            responsible_unit=1,
        )


class RequestHistoryTeacherSerializer(serializers.ModelSerializer):
    """
    История запросов справок реподавателя
    """
    request_title = serializers.CharField(source="get_request_title_display")
    responsible_unit = serializers.CharField(source="get_responsible_unit_display")
    datetime = serializers.SerializerMethodField(source="get_formatted_datetime")

    def get_datetime(self, obj):
        return obj.datetime.strftime("%d.%m.%Y %H:%M")

    class Meta:
        model = RequestTeacher
        fields = ("request_title", "request_text", "responsible_unit", "datetime", )

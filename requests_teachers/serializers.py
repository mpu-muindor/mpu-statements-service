from rest_framework import serializers
from requests_teachers.models import RequestTeacher


class ISSandComputerEquipmenterializer(serializers.Serializer):
    """
    Сериалайзер для следующих типов справок:
     - Получение нового компьютерного оборудования
     - Подключение компьютера, МФУ, телефона, WiFi
     - Обслуживание принтеров, МФУ
     - Вопрос по СЭД Directum и 1С
     - Вопрос по Личному кабинету
     - Прочее ИТ-обслуживание
    """
    fio = serializers.CharField()
    structural_unit = serializers.CharField()
    position = serializers.CharField()
    email = serializers.EmailField()
    work_phone = serializers.CharField(required=False, allow_null=True)
    mobile_phone = serializers.CharField()
    work_address_corpus = serializers.ChoiceField(choices=RequestTeacher.ADDRESSES)
    work_address_room = serializers.CharField()
    request_title = serializers.ChoiceField(choices=RequestTeacher.REQUESTS)
    request_text = serializers.CharField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)

    def save(self, **kwargs):
        text = f"Подразделение: {self.validated_data['structural_unit']}\nДолжность: \n," \
               f"Моб. телефон: {self.validated_data['mobile_phone']}\n" \
               f"Площадка: {dict(RequestTeacher.ADDRESSES).get(self.validated_data['work_address_corpus'])}\n" \
               f"Номер аудитории: {self.validated_data['work_address_room']}\n"
        if self.validated_data.get("request_text"):
            text += f'Заявка:\n{self.validated_data["request_text"]}'

        RequestTeacher.objects.create(
            request_title=self.validated_data['request_title'],
            request_text=text,
            responsible_unit=self.validated_data['work_address_corpus'],
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

from rest_framework import status, views
from rest_framework.response import Response

from requests_students.serializers import *


class EdRequestView(views.APIView):
    """
    Справка о прослушанных дисциплинах за период обучения (справка об обучении)
    """

    def post(self, request, format=None):
        serializer = EdRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusRequestView(views.APIView):
    """
    Справка о прохождении обучения в университете (о статусе обучающегося) по месту требования
    """

    def post(self, request, format=None):
        serializer = StatusRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SobesRequestView(views.APIView):
    """
    Справка в социальные учреждения (Пенсионный фонд, УСЗН и пр.)
    """

    def post(self, request, format=None):
        serializer = SobesRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CallRequestView(views.APIView):
    """
    Справка-вызов
    """

    def post(self, request, format=None):
        serializer = CallRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersDataRequestView(views.APIView):
    """
    Справка в социальные учреждения (Пенсионный фонд, УСЗН и пр.)
    """

    def post(self, request, format=None):
        serializer = PersDataRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassRestoreRequestView(views.APIView):
    """
    Заявление на восстановление магнитного пропуска
    """

    def post(self, request, format=None):
        serializer = PassRestoreRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PracticeSelectRequestView(views.APIView):
    """
    Выбор места практики
    """
    def get(self, request, format=None):
        text = "Данный вид практики в настоящее время недоступен"
        return Response(text, status=status.HTTP_400_BAD_REQUEST)


class PracticeLetterRequestView(views.APIView):
    """
    Заказ сопроводительного письма на прохождение практики
    """

    def post(self, request, format=None):
        serializer = PracticeLetterRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExtraAgreementRequestView(views.APIView):
    """
    Заключение дополнительного соглашения к договору об обучении
    """
    def get(self, request, format=None):
        text = "Данный вид услуги доступен только для студентов, обучающихся на платной договорной основе."
        return Response(text, status=status.HTTP_400_BAD_REQUEST)


class SendPaymentEduRequestView(views.APIView):
    """
    Отправка квитанции об оплате за обучение, неустойку (пени)
    """
    def get(self, request, format=None):
        text = "Данный вид услуги доступен только для студентов, обучающихся на платной договорной основе."
        return Response(text, status=status.HTTP_400_BAD_REQUEST)


class PrDonateRequestView(views.APIView):
    """
    Оформление дотации Мэрии г. Москвы
    """

    def post(self, request, format=None):
        serializer = PrDonateRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatHelpRequestView(views.APIView):
    """
    Заявка на оказание материальной помощи
    """

    def post(self, request, format=None):
        serializer = MatHelpRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocStipRequestView(views.APIView):
    """
    Оформление социальной стипендии
    """

    def post(self, request, format=None):
        serializer = SocStipRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArmyRequestView(views.APIView):
    """
    Запрос на получение в мобилизационном отделе справки (Приложение № 2)
    для получения отсрочки от призыва на военную службу в военном комиссариате
    """

    def post(self, request, format=None):
        serializer = ArmyRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FreeRequestView(views.APIView):
    """
    Произвольный запрос
    """

    def post(self, request, format=None):
        serializer = FreeRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MainPageRequestViewSet(views.APIView):
    """
    История запросов справок пользователя
    """

    def get(self, request, format=None):
        queryset = RequestStudent.objects.all()
        serializer = RequestHistoryStudentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressListViewSet(views.APIView):
    """
    Получение списка адресов
    """

    def get(self, request, format=None):
        queryset = Address.objects.all()
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestTypeListViewSet(views.APIView):
    """
    Получение списка типов заявок
    """

    def get(self, request, format=None):
        queryset = RequestStudentType.objects.all()
        serializer = RequestTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

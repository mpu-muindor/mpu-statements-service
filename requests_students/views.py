from rest_framework import status, views
from rest_framework.response import Response

from requests_students.serializers import *


class EdRequestView(views.APIView):
    """
    Справка о прослушанных дисциплинах за период обучения (справка об обучении)
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = EdRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class StatusRequestView(views.APIView):
    """
    Справка о прохождении обучения в университете (о статусе обучающегося) по месту требования
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = StatusRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class SobesRequestView(views.APIView):
    """
    Справка в социальные учреждения (Пенсионный фонд, УСЗН и пр.)
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = SobesRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class CallRequestView(views.APIView):
    """
    Справка-вызов
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = CallRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class PersDataRequestView(views.APIView):
    """
    Запрос на изменение персональных данных
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = PersDataRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class PassRestoreRequestView(views.APIView):
    """
    Заявление на восстановление магнитного пропуска
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = PassRestoreRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class PracticeSelectRequestView(views.APIView):
    """
    Выбор места практики
    """

    def get(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            return Response(
                {'message': 'Данный вид практики в настоящее время недоступен'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class PracticeLetterRequestView(views.APIView):
    """
    Заказ сопроводительного письма на прохождение практики
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = PracticeLetterRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class ExtraAgreementRequestView(views.APIView):
    """
    Заключение дополнительного соглашения к договору об обучении
    """

    def get(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            return Response(
                {'message': 'Данный вид услуги доступен только для студентов, обучающихся на платной договорной основе.'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class SendPaymentEduRequestView(views.APIView):
    """
    Отправка квитанции об оплате за обучение, неустойку (пени)
    """

    def get(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            return Response(
                {'message': 'Данный вид услуги доступен только для студентов, обучающихся на платной договорной основе.'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class PrDonateRequestView(views.APIView):
    """
    Оформление дотации Мэрии г. Москвы
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = PrDonateRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class MatHelpRequestView(views.APIView):
    """
    Заявка на оказание материальной помощи
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = MatHelpRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class SocStipRequestView(views.APIView):
    """
    Оформление социальной стипендии
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = SocStipRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class ArmyRequestView(views.APIView):
    """
    Запрос на получение в мобилизационном отделе справки (Приложение № 2)
    для получения отсрочки от призыва на военную службу в военном комиссариате
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = ArmyRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class FreeRequestView(views.APIView):
    """
    Произвольный запрос
    """

    def post(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            serializer = FreeRequestSerializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class RequestHistoryStudentView(views.APIView):
    """
    История запросов справок студента
    """

    def get(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            queryset = RequestStudent.objects.filter(user_uuid=user['id'])
            serializer = RequestHistoryStudentSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class AddressListViewSet(views.APIView):
    """
    Получение списка адресов
    """

    def get(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            queryset = Address.objects.all()
            serializer = AddressSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN)


class RequestTypeListViewSet(views.APIView):
    """
    Получение списка типов заявок
    """

    def get(self, request, format=None):
        user = request.user.user
        if user['user_type'] == 'student':
            queryset = RequestStudent.objects.filter()
            serializer = RequestHistoryStudentSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN)

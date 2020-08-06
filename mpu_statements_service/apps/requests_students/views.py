from rest_framework import status, views
from rest_framework.response import Response

from .serializers import *


class RequestStudentView(views.APIView):
    """
    Вью для создания доступных стравок
    """

    def post(self, request, serializer, format=None):
        user = request.user
        if user.user_type == 'student':
            serializer = serializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class NotAvailableRequestStudentView(views.APIView):
    """
    Недоступные справки
    """

    def get(self, request, format=None):
        user = request.user
        if user.user_type == 'student':
            return Response(
                {'message': 'Данный вид практики в настоящее время недоступен'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class PaymentRequestStudentView(views.APIView):
    """
    Справки для оплаты
    """

    def get(self, request, format=None):
        user = request.user
        if user.user_type == 'student':
            return Response(
                {'message': 'Данный вид услуги доступен только для студентов, обучающихся на платной договорной основе.'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class RequestHistoryStudentView(views.APIView):
    """
    История запросов справок студента
    """
    def get(self, request, format=None):
        user = request.user
        if user.user_type == 'student':
            queryset = RequestStudent.objects.filter(user_uuid=user.id)
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
        user = request.user
        if user.user_type == 'student':
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
        user = request.user
        if user.user_type == 'student':
            queryset = RequestStudent.objects.filter()
            serializer = RequestHistoryStudentSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN)

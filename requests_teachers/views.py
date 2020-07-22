from rest_framework import status, views
from rest_framework.response import Response

from requests_teachers.serializers import *


class ISSandComputerView(views.APIView):
    """
    Вью для следующих типов справок:
     - Получение нового компьютерного оборудования
     - Подключение компьютера, МФУ, телефона, WiFi
     - Обслуживание принтеров, МФУ
     - Вопрос по СЭД Directum и 1С
     - Вопрос по Личному кабинету
     - Прочее ИТ-обслуживание
    """

    def post(self, request, format=None):
        serializer = ISandComputersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkRequestsView(views.APIView):
    """
    Вью для следующих типов справок:
     - Справка с места работы
     - Справка на визу
     - Справка о стаже работы
     - Справка о количестве неиспользованных дней отпуска
     - Копия трудовой книжки
     - Копии документов из личного дела
     - Справка о работе на условиях внешнего совместительства для внесения стажа в трудовую книжку
     - Справка об отпуске по уходу за ребенком до 1,5 и 3 лет
    """

    def post(self, request, format=None):
        serializer = WorkRequestsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkPaymentsView(views.APIView):
    """
    Вью для следующих типов справок:
     - Справка по форме 2-НДФЛ
     - Справка о ежемесячных выплатах сотрудника, находящегося в отпуске по уходу за ребенком (декрет)
    """

    def post(self, request, format=None):
        serializer = WorkPaymentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestHistoryTeacherView(views.APIView):
    """
    История запросов справок преподавателя
    """

    def get(self, request, format=None):
        queryset = RequestTeacher.objects.all()
        serializer = RequestHistoryTeacherSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

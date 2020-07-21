from rest_framework import status, views
from rest_framework.response import Response

from requests_teachers.serializers import *


class NewComputerHardware(views.APIView):
    """
    Получение нового компьютерного оборудования
    """

    def post(self, request, format=None):
        serializer = ISSandComputerEquipmenterializer(data=request.data)
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

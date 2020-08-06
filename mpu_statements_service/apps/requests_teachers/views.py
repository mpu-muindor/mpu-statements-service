from rest_framework import status, views
from rest_framework.response import Response

from .serializers import *


class RequestTeacherView(views.APIView):
    """
    Вью для получения всех справок
    """

    def post(self, request, serializer, format=None):
        user = request.user
        if user.user_type == 'professor':
            serializer = serializer(data=request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN
        )


class RequestHistoryTeacherView(views.APIView):
    """
    История запросов справок преподавателя
    """

    def get(self, request, format=None):
        user = request.user
        if user.user_type == 'professor':
            queryset = RequestTeacher.objects.filter(user_uuid=user.id)
            serializer = RequestHistoryTeacherSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN)

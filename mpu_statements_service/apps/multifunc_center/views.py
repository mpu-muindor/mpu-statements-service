from rest_framework import views, status
from rest_framework.response import Response

from .models import Blank
from .serializers import BlankListSerializer
from django.db.models import Q


class StudBlanksView(views.APIView):
    def get(self, request):
        user = request.user
        if user.user_type == 'student':
            queryset = Blank.objects.filter(Q(category=Blank.student_category) |
                                            Q(category=Blank.doc_category))
            serializer = BlankListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN)


class TeacherBlanksView(views.APIView):
    def get(self, request):
        user = request.user
        if user.user_type == 'teacher':
            queryset = Blank.objects.filter(Q(category=Blank.teacher_category) |
                                            Q(category=Blank.doc_category))
            serializer = BlankListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'message': 'Данный сервис недоступен для Вашей учетной записи.'},
            status=status.HTTP_403_FORBIDDEN)

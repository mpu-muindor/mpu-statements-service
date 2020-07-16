from rest_framework import viewsets, status, views
from rest_framework.response import Response

from requests.models import *
from requests.serializers import *


class MainPageRequestViewSet(views.APIView):
    """
    История запросов справок пользователя.
    """

    def get(self, request, format=None):
        queryset = Request.objects.all()
        serializer = MainPageRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class EducationRequestViewSet(viewsets.ModelViewSet):
    """
    Справка о прослушанных дисциплинах за период обучения (справка об обучении).
    """

    queryset = EducationRequest.objects.all()
    serializer_class = EducationRequestTextSerializer

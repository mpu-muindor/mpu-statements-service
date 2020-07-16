from rest_framework import serializers
from requests.models import *


class EducationRequestTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationRequest
        fields = '__all__'


class MainPageRequestSerializer(serializers.ModelSerializer):
    # Django Model.get_FOO_display
    datetime = serializers.SerializerMethodField(source="get_formatted_datetime")
    request_title = serializers.ChoiceField(Request.REQUESTS)
    status = serializers.ChoiceField(Request.STATUSES)
    date_for_status = serializers.SerializerMethodField(source="get_date_for_status")
    address = serializers.ChoiceField(Request.ADDRESSES)

    def get_date_for_status(self, obj):
        return obj.date_for_status.strftime("%d.%m.%Y %H:%M")

    def get_datetime(self, obj):
        return obj.datetime.strftime("%d.%m.%Y %H:%M")

    class Meta:
        model = Request
        fields = ("datetime", "reg_number", "request_title", "request_text",
                  "status", "date_for_status", "address", "remark")

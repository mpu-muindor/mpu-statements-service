from django.contrib import admin
from requests_teachers.models import *


class RequestTeacherAdmin(admin.ModelAdmin):
    model = RequestTeacher
    list_display = ("user_uuid", "contacts", "datetime", "request_title", "request_text", "responsible_unit", )
    list_filter = ("request_title", "responsible_unit", )


admin.site.register(RequestTeacher, RequestTeacherAdmin)
admin.site.register(ResponsibleUnit)
admin.site.register(RequestTeacherType)

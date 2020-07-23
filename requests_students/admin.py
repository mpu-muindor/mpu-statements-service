from django.contrib import admin
from requests_students.models import *


class RequestStudentAdmin(admin.ModelAdmin):
    model = RequestStudent
    list_display = ("user_uuid", "contacts", "datetime", "reg_number", "request_title", "request_text",
                    "status", "date_for_status", "address", "remark")
    list_filter = ("status", "request_title", )


admin.site.register(RequestStudent, RequestStudentAdmin)
admin.site.register(Address)
admin.site.register(RequestStudentType)

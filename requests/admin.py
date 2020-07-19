from django.contrib import admin
from requests.models import *


class RequestsAdmin(admin.ModelAdmin):
    model = Request
    list_display = ("datetime", "reg_number", "request_title", "request_text",
                    "status", "date_for_status", "address", "remark")
    list_filter = ("status", "request_title", )


admin.site.register(Request, RequestsAdmin)
admin.site.register(Address)
admin.site.register(RequestType)

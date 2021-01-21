from django.contrib import admin
from django.utils.text import slugify
from unidecode import unidecode

from .models import Blank


class BlankAdmin(admin.ModelAdmin):
    list_display = ('title', 'blank', )
    prepopulated_fields = {'slug': ('title', )}

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(unidecode(form.cleaned_data['title']))
        obj.save()


admin.site.register(Blank, BlankAdmin)

"""mpu_statements_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView

from requests_students.views import *
from requests_teachers.views import RequestHistoryTeacherView, NewComputerHardware

urlpatterns = [
    # Swagger
    path('', TemplateView.as_view(
                template_name='swagger-ui.html',
                extra_context={'schema_url': 'openapi-schema'}
            ), name='swagger-ui'),

    # Admin
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Справки студентов
urlpatterns += [
    # Списки значений других таблиц
    path('statements/student/addresses/', AddressListViewSet.as_view()),
    path('statements/student/request_types/', RequestTypeListViewSet.as_view()),
    # История запросов
    path('statements/student/requests/', MainPageRequestViewSet.as_view()),
    # Центры по работе со студентами
    path('statements/student/education/', EdRequestView.as_view()),
    path('statements/student/status/', StatusRequestView.as_view()),
    path('statements/student/sobes/', SobesRequestView.as_view()),
    path('statements/student/call/', CallRequestView.as_view()),
    path('statements/student/pers_data/', PersDataRequestView.as_view()),
    path('statements/student/pass_restore/', PassRestoreRequestView.as_view()),
    # Практика
    path('statements/student/pract_select/', PracticeSelectRequestView.as_view()),
    path('statements/student/pract_letter/', PracticeLetterRequestView.as_view()),
    # Отдел платных образовательных услуг
    path('statements/student/extra_agreement/', ExtraAgreementRequestView.as_view()),
    path('statements/student/send_payment_edu/', SendPaymentEduRequestView.as_view()),
    # Профсоюзная организация
    path('statements/student/pr_donate/', PrDonateRequestView.as_view()),
    path('statements/student/pr_mathelp/', MatHelpRequestView.as_view()),
    path('statements/student/pr_socstip/', SocStipRequestView.as_view()),
    # Мобилизационный отдел
    path('statements/student/otsrochka/', ArmyRequestView.as_view()),
    # Прочее
    path('statements/student/free_request/', FreeRequestView.as_view()),

]

# Справки преподавателя
urlpatterns += [
    # История запросов
    path('statements/teacher/requests/', RequestHistoryTeacherView.as_view()),
    # История запросов справок преподавателя
    path('statements/teacher/new_hardware/', NewComputerHardware.as_view()),
    path('statements/teacher/new_computer/', NewComputerHardware.as_view()),
]

# Static files
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

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
from django.urls import include, path
from django.views.generic import TemplateView

from requests import views


urlpatterns = [
    # Swagger
    path('', TemplateView.as_view(
                template_name='swagger-ui.html',
                extra_context={'schema_url': 'openapi-schema'}
            ), name='swagger-ui'),

    # Admin
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Списки значений других таблиц
    path('statements/addresses/', views.AddressListViewSet.as_view()),
    path('statements/request_types/', views.RequestTypeListViewSet.as_view()),
    # История запросов
    path('statements/requests/', views.MainPageRequestViewSet.as_view()),
    # Центры по работе со студентами
    path('statements/student/education/', views.EdRequestView.as_view()),
    path('statements/student/status/', views.StatusRequestView.as_view()),
    path('statements/student/sobes/', views.SobesRequestView.as_view()),
    path('statements/student/call/', views.CallRequestView.as_view()),
    path('statements/student/pers_data/', views.PersDataRequestView.as_view()),
    path('statements/student/pass_restore/', views.PassRestoreRequestView.as_view()),
    # Практика
    path('statements/student/pract_select/', views.PracticeSelectRequestView.as_view()),
    path('statements/student/pract_letter/', views.PracticeLetterRequestView.as_view()),
    # Отдел платных образовательных услуг
    path('statements/student/extra_agreement/', views.ExtraAgreementRequestView.as_view()),
    path('statements/student/send_payment_edu/', views.SendPaymentEduRequestView.as_view()),
    # Профсоюзная организация
    path('statements/student/pr_donate/', views.PrDonateRequestView.as_view()),
    path('statements/student/pr_mathelp/', views.MatHelpRequestView.as_view()),
    path('statements/student/pr_socstip/', views.SocStipRequestView.as_view()),
    # Мобилизационный отдел
    path('statements/student/otsrochka/', views.ArmyRequestView.as_view()),
    # Прочее
    path('statements/student/free_request/', views.FreeRequestView.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

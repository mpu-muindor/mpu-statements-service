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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from requests import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # История запросов
    path('requests/', views.MainPageRequestViewSet.as_view()),
    # Центры по работе со студентами
    path('education/', views.EdRequestView.as_view()),
    path('status/', views.StatusRequestView.as_view()),
    path('sobes/', views.SobesRequestView.as_view()),
    path('call/', views.CallRequestView.as_view()),
    path('pers_data/', views.PersDataRequestView.as_view()),
    path('pass_restore/', views.PassRestoreRequestView.as_view()),
    # Практика
    path('pract_select/', views.PracticeSelectRequestView.as_view()),
    path('pract_letter/', views.PracticeLetterRequestView.as_view()),
    # Отдел платных образовательных услуг
    path('extra_agreement/', views.ExtraAgreementRequestView.as_view()),
    path('send_payment_edu/', views.SendPaymentEduRequestView.as_view()),
    # Профсоюзная организация
    path('pr_donate/', views.PrDonateRequestView.as_view()),
    path('pr_mathelp/', views.MatHelpRequestView.as_view()),
    path('pr_socstip/', views.SocStipRequestView.as_view()),
    # Мобилизационный отдел
    path('otsrochka/', views.ArmyRequestView.as_view()),
    # Прочее
    path('free_request/', views.FreeRequestView.as_view()),
]

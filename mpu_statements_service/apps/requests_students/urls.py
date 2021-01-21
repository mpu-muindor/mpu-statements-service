"""
Справки студентов
"""
from django.shortcuts import redirect
from django.urls import path
from .views import *
from .serializers import *


urlpatterns = [
    # Списки значений других таблиц
    path('addresses/', AddressListViewSet.as_view()),
    path('request_types/', RequestTypeListViewSet.as_view()),
    # История запросов
    path('requests/', RequestHistoryStudentView.as_view()),
    # Центры по работе со студентами
    path('education/', RequestStudentView.as_view(), {'serializer': EdRequestSerializerStudent}),
    path('status/', RequestStudentView.as_view(), {'serializer': StatusRequestSerializerStudent}),
    path('sobes/', RequestStudentView.as_view(), {'serializer': SobesRequestSerializerStudent}),
    path('call/', RequestStudentView.as_view(), {'serializer': CallRequestSerializerStudent}),
    path('pers_data/', RequestStudentView.as_view(), {'serializer': PersDataRequestSerializerStudent}),
    path('pass_restore/', RequestStudentView.as_view(), {'serializer': PassRestoreRequestSerializerStudent}),
    # Практика
    path('pract_select/', NotAvailableRequestStudentView.as_view(), {'serializer': EdRequestSerializerStudent}),
    path('pract_letter/', RequestStudentView.as_view(), {'serializer': PracticeLetterRequestSerializerStudent}),
    # Отдел платных образовательных услуг
    path('extra_agreement/', PaymentRequestStudentView.as_view(), {'serializer': EdRequestSerializerStudent}),
    path('send_payment_edu/', PaymentRequestStudentView.as_view(), {'serializer': EdRequestSerializerStudent}),
    # Профсоюзная организация
    path('pr_mathelp/', RequestStudentView.as_view(), {'serializer': MatHelpRequestSerializerStudent}),
    path('pr_socstip/', RequestStudentView.as_view(), {'serializer': SocStipRequestSerializerStudent}),
    # Мобилизационный отдел
    path('otsrochka/', RequestStudentView.as_view(), {'serializer': ArmyRequestSerializerStudent}),
    # Прочее
    path('free_request/', RequestStudentView.as_view(), {'serializer': FreeRequestSerializerStudent}),

    # Новое
    path('diplom/', RequestStudentView.as_view(), {'serializer': DiplomSerializer}),
    path('passport_data/', RequestStudentView.as_view(), {'serializer': PassportDataSerializer}),
    path('prof/', lambda request: redirect('https://lk.eseur.ru/signup/', permanent=True)),
]

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
from requests_teachers.views import RequestHistoryTeacherView, ISSandComputerView, WorkRequestsView, WorkPaymentsView

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
    path('student/addresses/', AddressListViewSet.as_view()),
    path('student/request_types/', RequestTypeListViewSet.as_view()),
    # История запросов
    path('student/requests/', RequestHistoryStudentView.as_view()),
    # Центры по работе со студентами
    path('student/education/', EdRequestView.as_view()),
    path('student/status/', StatusRequestView.as_view()),
    path('student/sobes/', SobesRequestView.as_view()),
    path('student/call/', CallRequestView.as_view()),
    path('student/pers_data/', PersDataRequestView.as_view()),
    path('student/pass_restore/', PassRestoreRequestView.as_view()),
    # Практика
    path('student/pract_select/', PracticeSelectRequestView.as_view()),
    path('student/pract_letter/', PracticeLetterRequestView.as_view()),
    # Отдел платных образовательных услуг
    path('student/extra_agreement/', ExtraAgreementRequestView.as_view()),
    path('student/send_payment_edu/', SendPaymentEduRequestView.as_view()),
    # Профсоюзная организация
    path('student/pr_donate/', PrDonateRequestView.as_view()),
    path('student/pr_mathelp/', MatHelpRequestView.as_view()),
    path('student/pr_socstip/', SocStipRequestView.as_view()),
    # Мобилизационный отдел
    path('student/otsrochka/', ArmyRequestView.as_view()),
    # Прочее
    path('student/free_request/', FreeRequestView.as_view()),
]

# Справки преподавателя
urlpatterns += [
    # История запросов справок преподавателя
    path('teacher/requests/', RequestHistoryTeacherView.as_view()),

    # Получение нового компьютерного оборудования
    path('teacher/new_hardware/', ISSandComputerView.as_view()),
    # Подключение компьютера, МФУ, телефона, WiFi
    path('teacher/new_computer/', ISSandComputerView.as_view()),
    # Обслуживание принтеров, МФУ
    path('teacher/help_mfu/', ISSandComputerView.as_view()),
    # Вопрос по СЭД Directum и 1С
    path('teacher/help_1c/', ISSandComputerView.as_view()),
    # Вопрос по Личному кабинету
    path('teacher/help_lk/', ISSandComputerView.as_view()),
    # Прочее ИТ-обслуживание
    path('teacher/other_it/', ISSandComputerView.as_view()),

    # Справка с места работы
    path('teacher/work_request/', WorkRequestsView.as_view()),
    # Справка на визу
    path('teacher/work_visa/', WorkRequestsView.as_view()),
    # Справка о стаже работы
    path('teacher/work_expirience/', WorkRequestsView.as_view()),
    # Справка о количестве неиспользованных дней отпуска
    path('teacher/work_holiday/', WorkRequestsView.as_view()),
    # Копия трудовой книжки
    path('teacher/work_tk/', WorkRequestsView.as_view()),
    # Копии документов из личного дела
    path('teacher/work_copy/', WorkRequestsView.as_view()),
    # Справка о работе на условиях внешнего совместительства для внесения стажа в трудовую книжку
    path('teacher/work_add_exp/', WorkRequestsView.as_view()),

    # Справка по форме 2-НДФЛ
    path('teacher/2-ndfl/', WorkPaymentsView.as_view()),
    # Справка о выплате (не выплате) единовременного пособия на рождение ребенка
    path('teacher/payment_child/', WorkPaymentsView.as_view()),
    # Справка об отпуске по уходу за ребенком до 1,5 и 3 лет
    path('teacher/work_child/', WorkRequestsView.as_view()),
    # Справка о ежемесячных выплатах сотрудника, находящегося в отпуске по уходу за ребенком (декрет)
    path('teacher/decree/', WorkPaymentsView.as_view()),
]

# Static files
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

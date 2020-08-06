"""
Справки преподавателей
"""
from django.urls import path
from .views import *
from .serializers import *


urlpatterns = [
    # История запросов справок преподавателя
    path('requests/', RequestHistoryTeacherView.as_view()),

    # Получение нового компьютерного оборудования
    path('new_hardware/', RequestTeacherView.as_view(), {'serializer': ISandComputersSerializer}),
    # Подключение компьютера, МФУ, телефона, WiFi
    path('new_computer/', RequestTeacherView.as_view(), {'serializer': ISandComputersSerializer}),
    # Обслуживание принтеров, МФУ
    path('help_mfu/', RequestTeacherView.as_view(), {'serializer': ISandComputersSerializer}),
    # Вопрос по СЭД Directum и 1С
    path('help_1c/', RequestTeacherView.as_view(), {'serializer': ISandComputersSerializer}),
    # Вопрос по Личному кабинету
    path('help_lk/', RequestTeacherView.as_view(), {'serializer': ISandComputersSerializer}),
    # Прочее ИТ-обслуживание
    path('other_it/', RequestTeacherView.as_view(), {'serializer': ISandComputersSerializer}),

    # Справка с места работы
    path('work_request/', RequestTeacherView.as_view(), {'serializer': WorkRequestsSerializer}),
    # Справка на визу
    path('work_visa/', RequestTeacherView.as_view(), {'serializer': WorkRequestsSerializer}),
    # Справка о стаже работы
    path('work_expirience/', RequestTeacherView.as_view(), {'serializer': WorkRequestsSerializer}),
    # Справка о количестве неиспользованных дней отпуска
    path('work_holiday/', RequestTeacherView.as_view(), {'serializer': WorkRequestsSerializer}),
    # Копия трудовой книжки
    path('work_tk/', RequestTeacherView.as_view(), {'serializer': WorkRequestsSerializer}),
    # Копии документов из личного дела
    path('work_copy/', RequestTeacherView.as_view(), {'serializer': WorkRequestsSerializer}),
    # Справка о работе на условиях внешнего совместительства для внесения стажа в трудовую книжку
    path('work_add_exp/', RequestTeacherView.as_view(), {'serializer': WorkRequestsSerializer}),

    # Справка по форме 2-НДФЛ
    path('2-ndfl/', RequestTeacherView.as_view(), {'serializer': WorkPaymentsSerializer}),
    # Справка о выплате (не выплате) единовременного пособия на рождение ребенка
    path('payment_child/', RequestTeacherView.as_view(), {'serializer': WorkPaymentsSerializer}),
    # Справка об отпуске по уходу за ребенком до 1,5 и 3 лет
    path('work_child/', RequestTeacherView.as_view(), {'serializer': WorkPaymentsSerializer}),
    # Справка о ежемесячных выплатах сотрудника, находящегося в отпуске по уходу за ребенком (декрет)
    path('decree/', RequestTeacherView.as_view(), {'serializer': WorkPaymentsSerializer}),
]
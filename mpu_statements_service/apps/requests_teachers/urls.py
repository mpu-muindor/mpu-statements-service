"""
Справки преподавателей
"""
from .views import *
from django.urls import path


urlpatterns = [
    # История запросов справок преподавателя
    path('requests/', RequestHistoryTeacherView.as_view()),

    # Получение нового компьютерного оборудования
    path('new_hardware/', ISSandComputerView.as_view()),
    # Подключение компьютера, МФУ, телефона, WiFi
    path('new_computer/', ISSandComputerView.as_view()),
    # Обслуживание принтеров, МФУ
    path('help_mfu/', ISSandComputerView.as_view()),
    # Вопрос по СЭД Directum и 1С
    path('help_1c/', ISSandComputerView.as_view()),
    # Вопрос по Личному кабинету
    path('help_lk/', ISSandComputerView.as_view()),
    # Прочее ИТ-обслуживание
    path('other_it/', ISSandComputerView.as_view()),

    # Справка с места работы
    path('work_request/', WorkRequestsView.as_view()),
    # Справка на визу
    path('work_visa/', WorkRequestsView.as_view()),
    # Справка о стаже работы
    path('work_expirience/', WorkRequestsView.as_view()),
    # Справка о количестве неиспользованных дней отпуска
    path('work_holiday/', WorkRequestsView.as_view()),
    # Копия трудовой книжки
    path('work_tk/', WorkRequestsView.as_view()),
    # Копии документов из личного дела
    path('work_copy/', WorkRequestsView.as_view()),
    # Справка о работе на условиях внешнего совместительства для внесения стажа в трудовую книжку
    path('work_add_exp/', WorkRequestsView.as_view()),

    # Справка по форме 2-НДФЛ
    path('2-ndfl/', WorkPaymentsView.as_view()),
    # Справка о выплате (не выплате) единовременного пособия на рождение ребенка
    path('payment_child/', WorkPaymentsView.as_view()),
    # Справка об отпуске по уходу за ребенком до 1,5 и 3 лет
    path('work_child/', WorkRequestsView.as_view()),
    # Справка о ежемесячных выплатах сотрудника, находящегося в отпуске по уходу за ребенком (декрет)
    path('decree/', WorkPaymentsView.as_view()),
]
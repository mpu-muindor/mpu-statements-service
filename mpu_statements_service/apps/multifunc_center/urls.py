from django.urls import path
from .views import StudBlanksView, TeacherBlanksView

urlpatterns = [
    path('stud_blanks/', StudBlanksView.as_view(), name='stud_blanks_list'),
    path('teacher_blanks/', TeacherBlanksView.as_view(), name='stud_blanks_list'),
]
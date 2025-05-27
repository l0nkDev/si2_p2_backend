from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from server.backend import views

urlpatterns = [
    path('admin/students/', views.StudentList.as_view()),
    path('admin/students/<int:pk>/', views.StudentDetail.as_view()),
    path('admin/teachers/', views.TeacherList.as_view()),
    path('admin/teachers/<int:pk>/', views.TeacherDetail.as_view()),
    path('admin/users/', views.UserList.as_view()),
    path('admin/users/<int:pk>/', views.UserDetail.as_view()),
    path('admin/classes/', views.CreateClassesForYear.as_view()),
    path('users/self/', views.UserSelf.as_view()),
    path('auth/login/', views.UserLogin.as_view()),
    path('teacher/scores/', views.ScoreList.as_view()),
    path('teacher/scores/<int:pk>/', views.ScoreDetail.as_view()),
    path('teacher/assistance/', views.AssistanceList.as_view()),
    path('teacher/assistance/<int:pk>/', views.AssistanceDetail.as_view()),
    path('teacher/participation/', views.ParticipationList.as_view()),
    path('teacher/participation/<int:pk>/', views.ParticipationDetail.as_view()),
    path('teacher/subjects/', views.TeachersClasses.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
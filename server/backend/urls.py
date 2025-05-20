from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from server.backend import views

urlpatterns = [
    path('students/', views.StudentList.as_view()),
    path('students/<int:pk>/', views.StudentDetail.as_view()),
    path('teachers/', views.TeacherList.as_view()),
    path('teachers/<int:pk>/', views.TeacherDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/self/', views.UserSelf.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('auth/login/', views.UserLogin.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
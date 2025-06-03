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
    
    path('admin/subjectareas/', views.AreaList.as_view()),
    path('admin/subjectareas/list/', views.SubjectAreaList.as_view()),
    
    path('admin/subjects/', views.SubjectList.as_view()),
    path('admin/subjects/<int:pk>/', views.SubjectDetail.as_view()),
    
    path('admin/classsession/', views.ClassSessionList.as_view()),
    path('admin/classsession/<int:pk>/', views.ClassSessionDetail.as_view()),
    
    path('admin/classes/create/', views.CreateClassesForYear.as_view()),
    path('admin/classes/', views.ClassList.as_view()),
    path('admin/classes/<int:pk>/assign/', views.AssignClassSubject.as_view()),
    
    path('admin/logs/', views.LogsList.as_view()),
    
    path('admin/backups/', views.BackupsList.as_view()),
    
    path('admin/reports/', views.ReporteShow.as_view()),
    path('admin/reports/new/', views.ReporteList.as_view()),
    
    path('users/self/', views.UserSelf.as_view()),
    
    path('auth/login/', views.UserLogin.as_view()),
    path('auth/logout/', views.UserLogout.as_view()),
    
    path('teacher/scores/', views.ScoreList.as_view()),
    path('teacher/scores/<int:pk>/', views.ScoreDetail.as_view()),
    
    path('teacher/assistance/', views.AssistanceList.as_view()),
    path('teacher/assistance/<int:pk>/', views.AssistanceDetail.as_view()),
    
    path('teacher/participation/', views.ParticipationList.as_view()),
    path('teacher/participation/<int:pk>/', views.ParticipationDetail.as_view()),
    
    path('teacher/subjects/', views.TeachersClasses.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/assistance/', views.ClassAssistance.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/assistance/sessions/', views.TeachersSessions.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/assistance/sessions/today/', views.TeacherSessionStatus.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/assistance/', views.ClassAssistanceStudent.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/assistance/sessions/', views.StudentsSessions.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/assistance/sessions/today/', views.StudentSessionStatus.as_view()),
    
    path('teacher/subjects/<int:pk>/<int:_class>/participation/', views.ClassParticipation.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/participation/', views.StudentParticipation.as_view()),
    
    path('teacher/subjects/<int:pk>/<int:_class>/scores/', views.ClassScores.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/scores/targets/', views.ClassScoreTargets.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/scores/', views.StudentScores.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/scores/targets/', views.StudentScoreTargets.as_view()),
    
    path('student/subjects/', views.StudentsClasses.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/participation/', views.ClassAssistance.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
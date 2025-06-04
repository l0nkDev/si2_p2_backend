from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from server.backend import views
from server.backend.core.automation.views import automation
import server.backend.core.views as core
import server.backend.admin.views as admin
import server.backend.grades.views as grades
import server.backend.participations.views as participations
import server.backend.assistance.views as assistance

urlpatterns = [
    path('admin/students/', core.StudentList.as_view()),
    path('admin/students/<int:pk>/', core.StudentDetail.as_view()),
    
    path('admin/teachers/', core.TeacherList.as_view()),
    path('admin/teachers/<int:pk>/', core.TeacherDetail.as_view()),
    
    path('admin/users/', core.UserList.as_view()),
    path('admin/users/<int:pk>/', core.UserDetail.as_view()),
    
    path('admin/subjectareas/', core.AreaList.as_view()),
    path('admin/subjectareas/list/', core.SubjectAreaList.as_view()),
    
    path('admin/subjects/', core.SubjectList.as_view()),
    path('admin/subjects/<int:pk>/', core.SubjectDetail.as_view()),
    
    path('admin/classsession/', assistance.ClassSessionList.as_view()),
    path('admin/classsession/<int:pk>/', assistance.ClassSessionDetail.as_view()),
    
    path('admin/classes/', core.ClassList.as_view()),
    path('admin/classes/<int:pk>/assign/', core.AssignClassSubject.as_view()),
    
    path('admin/logs/', admin.LogsList.as_view()),
    
    path('admin/backups/', admin.BackupsList.as_view()),
    
    path('admin/reports/', admin.ReporteShow.as_view()),
    path('admin/reports/new/', admin.ReporteList.as_view()),
    
    path('users/self/', core.UserSelf.as_view()),
    
    path('auth/login/', core.UserLogin.as_view()),
    path('auth/logout/', core.UserLogout.as_view()),
    
    path('teacher/scores/', grades.ScoreList.as_view()),
    path('teacher/scores/<int:pk>/', grades.ScoreDetail.as_view()),
    
    path('teacher/assistance/', assistance.AssistanceList.as_view()),
    path('teacher/assistance/<int:pk>/', assistance.AssistanceDetail.as_view()),
    
    path('teacher/participation/', participations.ParticipationList.as_view()),
    path('teacher/participation/<int:pk>/', participations.ParticipationDetail.as_view()),
    
    path('teacher/subjects/', core.TeachersClasses.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/assistance/', assistance.ClassAssistance.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/assistance/sessions/', assistance.TeachersSessions.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/assistance/sessions/today/', assistance.TeacherSessionStatus.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/assistance/', assistance.ClassAssistanceStudent.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/assistance/sessions/', assistance.StudentsSessions.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/assistance/sessions/today/', assistance.StudentSessionStatus.as_view()),
    
    path('teacher/subjects/<int:pk>/<int:_class>/participation/', participations.ClassParticipation.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/participation/', participations.StudentParticipation.as_view()),
    
    path('teacher/subjects/<int:pk>/<int:_class>/scores/', grades.ClassScores.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/scores/targets/', grades.ClassScoreTargets.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/scores/', grades.StudentScores.as_view()),
    path('student/subjects/<int:pk>/<int:_class>/scores/targets/', grades.StudentScoreTargets.as_view()),
    
    path('student/subjects/', core.StudentsClasses.as_view()),
    path('teacher/subjects/<int:pk>/<int:_class>/participation/', assistance.ClassAssistance.as_view()),
    path('students/<int:pk>/', core.StudentProfile.as_view()),
    
    path('admin/auto/', automation.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
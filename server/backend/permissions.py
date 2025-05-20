from rest_framework import permissions
from server.backend.views import User

class IsLoggedIn(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1])
        except:
            return False
        print(user)
        return True

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1])
        except:
            return False
        print(user)
        return user.role == 'A' or user.role == 'O'  

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1])
        except:
            return False
        print(user)
        return user.role == 'S' or user.role == 'O'    

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1])
        except:
            return False
        print(user)
        return user.role == 'T' or user.role == 'O'    

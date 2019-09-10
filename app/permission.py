from rest_framework import permissions
from .models import MyUser

class JobSeekerAuthentication(permissions.BasePermission):
    """Authorization Permission class for Jobseeker"""
    message = 'Employer or Company has no permission dor this function.'
    def has_permission(self, request, view):
        try:
            return request.user and request.user.id and request.user.is_authenticated and MyUser.objects.get(email=request.user ,user_type="Job Seeker")
        except Exception as e:
            print("invalid user",e)    


class EmployerAuthentication(permissions.BasePermission):
    """Authorization Permission class for Company"""
    message = 'Employer or Company has no permission dor this function.'
    def has_permission(self, request, view):
        try:
            return request.user and request.user.id and request.user.is_authenticated and MyUser.objects.get(email=request.user ,user_type="Company")
        except Exception as e:
            print("invalid user",e)    




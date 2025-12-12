from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'doctor'

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'patient'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'

class IsOwnerOrDoctor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Les docteurs peuvent voir les dossiers de leurs patients
        if request.user.user_type == 'doctor':
            return True
        # Les patients ne peuvent voir que leurs propres dossiers
        if hasattr(obj, 'patient'):
            return obj.patient.user == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False

class IsPatientOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
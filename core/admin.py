from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'phone_number', 
                                                  'date_of_birth', 'address')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 
                                   'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('medical_license', 'specialization', 'hospital', 'is_verified')
    list_filter = ('specialization', 'is_verified')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'medical_license')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'emergency_contact')
    list_filter = ('blood_type',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'insurance_number')

admin.site.register(User, CustomUserAdmin)
from django.contrib import admin
from .models import MedicalRecord, MedicalTest

class MedicalTestInline(admin.TabularInline):
    model = MedicalTest
    extra = 1

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'record_type', 'date', 'created_by')
    list_filter = ('record_type', 'date', 'is_emergency')
    search_fields = ('title', 'patient__user__email', 'patient__user__first_name', 
                    'patient__user__last_name', 'diagnosis')
    date_hierarchy = 'date'
    inlines = [MedicalTestInline]

@admin.register(MedicalTest)
class MedicalTestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'record', 'test_date', 'lab_name')
    list_filter = ('test_date', 'lab_name')
    search_fields = ('test_name', 'record__title', 'lab_name')
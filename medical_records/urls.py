from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet, PatientSearchView

app_name = 'medical_records'

router = DefaultRouter()
router.register(r'', MedicalRecordViewSet, basename='medical-record')

urlpatterns = [
    path('', include(router.urls)),
    path('search/patients/', PatientSearchView.as_view(), name='patient-search'),
]
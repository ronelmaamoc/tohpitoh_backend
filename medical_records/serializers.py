from rest_framework import serializers
from .models import MedicalRecord, MedicalTest
from core.serializers import PatientProfileSerializer, DoctorProfileSerializer

class MedicalTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTest
        fields = '__all__'

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer(read_only=True)
    created_by = DoctorProfileSerializer(read_only=True)
    tests = MedicalTestSerializer(many=True, read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ('patient', 'created_by', 'date')

class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ('record_type', 'title', 'description', 'diagnosis', 
                 'prescription', 'notes', 'file', 'is_emergency')
from rest_framework import generics, viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
import io

from .models import MedicalRecord, MedicalTest
from .serializers import MedicalRecordSerializer, MedicalRecordCreateSerializer
from .pdf_generator import generate_medical_record_pdf
from core.permissions import IsDoctor, IsPatient, IsOwnerOrDoctor
from core.models import Patient, Doctor

class MedicalRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrDoctor]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'doctor':
            # Les docteurs voient tous les dossiers
            return MedicalRecord.objects.all()
        elif user.user_type == 'patient':
            # Les patients voient seulement leurs dossiers
            patient = Patient.objects.get(user=user)
            return MedicalRecord.objects.filter(patient=patient)
        return MedicalRecord.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MedicalRecordCreateSerializer
        return MedicalRecordSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        
        if user.user_type == 'doctor':
            doctor = Doctor.objects.get(user=user)
            patient_id = self.request.data.get('patient_id')
            
            if not patient_id:
                raise serializers.ValidationError({"patient_id": "Ce champ est requis."})
            
            try:
                patient = Patient.objects.get(id=patient_id)
            except Patient.DoesNotExist:
                raise serializers.ValidationError({"patient_id": "Patient non trouvé."})
            
            serializer.save(patient=patient, created_by=doctor)
        else:
            # Un patient ne peut pas créer son propre dossier médical
            raise serializers.ValidationError({"detail": "Vous n'avez pas la permission de créer des dossiers médicaux."})
    
    @action(detail=False, methods=['get'])
    def my_records(self, request):
        """Endpoint pour les patients pour voir leurs propres dossiers"""
        if request.user.user_type != 'patient':
            return Response({"detail": "Réservé aux patients."}, status=403)
        
        patient = Patient.objects.get(user=request.user)
        records = MedicalRecord.objects.filter(patient=patient)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Télécharger un dossier médical en PDF"""
        record = self.get_object()
        
        # Vérifier les permissions
        if request.user.user_type == 'patient' and record.patient.user != request.user:
            return Response({"detail": "Accès non autorisé."}, status=403)
        
        # Générer le PDF
        buffer = generate_medical_record_pdf([record], record.patient)
        
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"dossier_medical_{record.patient.user.last_name}_{record.id}.pdf"
        )
    
    @action(detail=False, methods=['get'])
    def download_all_pdf(self, request):
        """Télécharger tous les dossiers d'un patient en PDF"""
        user = request.user
        
        if user.user_type == 'patient':
            patient = Patient.objects.get(user=user)
            records = MedicalRecord.objects.filter(patient=patient)
        elif user.user_type == 'doctor':
            patient_id = request.query_params.get('patient_id')
            if not patient_id:
                return Response({"detail": "patient_id requis."}, status=400)
            
            try:
                patient = Patient.objects.get(id=patient_id)
                records = MedicalRecord.objects.filter(patient=patient)
            except Patient.DoesNotExist:
                return Response({"detail": "Patient non trouvé."}, status=404)
        else:
            return Response({"detail": "Accès non autorisé."}, status=403)
        
        # Générer le PDF
        buffer = generate_medical_record_pdf(records, patient)
        
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"carnet_medical_complet_{patient.user.last_name}.pdf"
        )

class PatientSearchView(generics.ListAPIView):
    """Vue pour rechercher des patients (réservée aux docteurs)"""
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 
                    'patient__user__email', 'patient__user__phone_number']
    
    def get_queryset(self):
        return MedicalRecord.objects.all()
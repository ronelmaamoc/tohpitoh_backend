from django.db import models
from core.models import Patient, Doctor

class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = (
        ('consultation', 'Consultation'),
        ('prescription', 'Ordonnance'),
        ('test', 'Test Médical'),
        ('vaccination', 'Vaccination'),
        ('surgery', 'Chirurgie'),
        ('hospitalization', 'Hospitalisation'),
        ('other', 'Autre'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    created_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='created_records')
    date = models.DateTimeField(auto_now_add=True)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    file = models.FileField(upload_to='medical_files/%Y/%m/%d/', blank=True, null=True)
    is_emergency = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - {self.patient.user.get_full_name()}"

class MedicalTest(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='tests')
    test_name = models.CharField(max_length=200)
    test_date = models.DateField()
    result = models.TextField()
    unit = models.CharField(max_length=50, blank=True)
    normal_range = models.CharField(max_length=100, blank=True)
    lab_name = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to='test_results/%Y/%m/%d/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.test_name} - {self.record.patient.user.get_full_name()}"
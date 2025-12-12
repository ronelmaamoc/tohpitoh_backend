from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from datetime import datetime
import os

def register_fonts():
    """Enregistrer les polices Unicode"""
    try:
        # Chercher des polices Unicode (Arial Unicode MS ou DejaVu)
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            'C:/Windows/Fonts/arial.ttf',
            '/System/Library/Fonts/Arial.ttf'
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                pdfmetrics.registerFont(TTFont('DejaVu', path))
                return 'DejaVu'
    except:
        pass
    return 'Helvetica'

def generate_medical_record_pdf(medical_records, patient):
    """Générer un PDF du dossier médical"""
    buffer = io.BytesIO()
    
    # Créer le document
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=72)
    
    # Préparer les styles
    styles = getSampleStyleSheet()
    font_name = register_fonts()
    
    # Styles personnalisés
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName=font_name
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=12,
        fontName=font_name
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName=font_name
    )
    
    # Contenu du PDF
    story = []
    
    # En-tête
    story.append(Paragraph("TOHPITOH - Carnet Médical", title_style))
    story.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Informations patient
    story.append(Paragraph("INFORMATIONS PATIENT", heading_style))
    
    patient_data = [
        ["Nom complet:", f"{patient.user.first_name} {patient.user.last_name}"],
        ["Date de naissance:", patient.user.date_of_birth.strftime('%d/%m/%Y') if patient.user.date_of_birth else "Non renseignée"],
        ["Email:", patient.user.email],
        ["Téléphone:", patient.user.phone_number or "Non renseigné"],
        ["Adresse:", patient.user.address or "Non renseignée"],
        ["Groupe sanguin:", patient.blood_type or "Non renseigné"],
        ["Allergies:", patient.allergies or "Aucune connue"],
        ["Maladies chroniques:", patient.chronic_diseases or "Aucune"],
        ["Contact d'urgence:", patient.emergency_contact or "Non renseigné"],
    ]
    
    if patient.height and patient.weight:
        bmi = patient.calculate_bmi()
        patient_data.append(["IMC (BMI):", f"{bmi:.2f}"])
    
    patient_table = Table(patient_data, colWidths=[3*cm, 10*cm])
    patient_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 30))
    
    # Historique médical
    if medical_records:
        story.append(Paragraph("HISTORIQUE MÉDICAL", heading_style))
        
        for record in medical_records:
            # Informations du dossier
            record_info = [
                ["Date:", record.date.strftime('%d/%m/%Y %H:%M')],
                ["Type:", record.get_record_type_display()],
                ["Titre:", record.title],
            ]
            
            if record.created_by:
                record_info.append(["Créé par:", f"Dr. {record.created_by.user.get_full_name()}"])
            
            record_table = Table(record_info, colWidths=[2*cm, 11*cm])
            record_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            story.append(record_table)
            
            # Description
            if record.description:
                story.append(Paragraph("<b>Description:</b>", normal_style))
                story.append(Paragraph(record.description, normal_style))
            
            # Diagnostic
            if record.diagnosis:
                story.append(Paragraph("<b>Diagnostic:</b>", normal_style))
                story.append(Paragraph(record.diagnosis, normal_style))
            
            # Prescription
            if record.prescription:
                story.append(Paragraph("<b>Prescription:</b>", normal_style))
                story.append(Paragraph(record.prescription, normal_style))
            
            # Notes
            if record.notes:
                story.append(Paragraph("<b>Notes:</b>", normal_style))
                story.append(Paragraph(record.notes, normal_style))
            
            # Tests médicaux associés
            if record.tests.exists():
                story.append(Paragraph("<b>Tests médicaux:</b>", normal_style))
                
                test_data = [["Test", "Date", "Résultat", "Valeurs normales"]]
                for test in record.tests.all():
                    test_data.append([
                        test.test_name,
                        test.test_date.strftime('%d/%m/%Y'),
                        test.result,
                        test.normal_range or "N/A"
                    ])
                
                test_table = Table(test_data, colWidths=[3*cm, 2.5*cm, 4*cm, 3*cm])
                test_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), font_name),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                
                story.append(test_table)
            
            story.append(Spacer(1, 15))
    
    else:
        story.append(Paragraph("Aucun dossier médical trouvé.", normal_style))
    
    # Pied de page
    story.append(Spacer(1, 30))
    story.append(Paragraph("*** Ce document est confidentiel et protégé par le secret médical ***", 
                          ParagraphStyle('Footer', parent=normal_style, alignment=TA_CENTER)))
    story.append(Paragraph(f"Page 1/1", 
                          ParagraphStyle('PageNumber', parent=normal_style, alignment=TA_CENTER)))
    
    # Générer le PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer
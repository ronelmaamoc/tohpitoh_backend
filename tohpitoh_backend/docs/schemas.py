"""
Schémas OpenAPI personnalisés pour la documentation
"""
from drf_yasg import openapi

# Tags pour organiser les endpoints
TAGS = [
    {
        'name': 'Authentication',
        'description': 'Endpoints pour l\'authentification des utilisateurs'
    },
    {
        'name': 'Patients',
        'description': 'Gestion des profils patients'
    },
    {
        'name': 'Doctors',
        'description': 'Gestion des profils médecins'
    },
    {
        'name': 'Medical Records',
        'description': 'Gestion des dossiers médicaux'
    },
    {
        'name': 'Medical Tests',
        'description': 'Gestion des tests médicaux'
    },
    {
        'name': 'PDF Generation',
        'description': 'Génération de PDF pour les dossiers médicaux'
    },
]

# Réponses communes
RESPONSES = {
    '200': openapi.Response(
        description='Succès',
        schema=openapi.Schema(type=openapi.TYPE_OBJECT)
    ),
    '201': openapi.Response(
        description='Créé avec succès',
        schema=openapi.Schema(type=openapi.TYPE_OBJECT)
    ),
    '400': openapi.Response(
        description='Requête invalide',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING),
                'errors': openapi.Schema(type=openapi.TYPE_OBJECT),
            }
        )
    ),
    '401': openapi.Response(
        description='Non authentifié',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    ),
    '403': openapi.Response(
        description='Permission refusée',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    ),
    '404': openapi.Response(
        description='Non trouvé',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    ),
    '500': openapi.Response(
        description='Erreur serveur',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    ),
}

# Schémas de sécurité
SECURITY_SCHEMES = {
    'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
        'description': 'JWT Token au format: Bearer {token}'
    }
}

# Paramètres de pagination
PAGINATION_PARAMS = [
    openapi.Parameter(
        'page',
        openapi.IN_QUERY,
        description="Numéro de page",
        type=openapi.TYPE_INTEGER,
        default=1,
    ),
    openapi.Parameter(
        'page_size',
        openapi.IN_QUERY,
        description="Nombre d'éléments par page",
        type=openapi.TYPE_INTEGER,
        default=20,
    ),
]

# Paramètres de recherche et filtre
SEARCH_PARAMS = [
    openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description="Recherche textuelle",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        'ordering',
        openapi.IN_QUERY,
        description="Tri des résultats (ex: -date, title)",
        type=openapi.TYPE_STRING,
    ),
]

# Schémas de modèles
SCHEMA_DEFINITIONS = {
    'User': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, readOnly=True),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'user_type': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=['patient', 'doctor', 'admin']
            ),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'date_of_birth': openapi.Schema(
                type=openapi.TYPE_STRING,
                format='date'
            ),
            'address': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    'Patient': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, readOnly=True),
            'user': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                ref='#/definitions/User'
            ),
            'blood_type': openapi.Schema(type=openapi.TYPE_STRING),
            'height': openapi.Schema(type=openapi.TYPE_NUMBER),
            'weight': openapi.Schema(type=openapi.TYPE_NUMBER),
            'allergies': openapi.Schema(type=openapi.TYPE_STRING),
            'chronic_diseases': openapi.Schema(type=openapi.TYPE_STRING),
            'emergency_contact': openapi.Schema(type=openapi.TYPE_STRING),
            'emergency_phone': openapi.Schema(type=openapi.TYPE_STRING),
            'insurance_number': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    'Doctor': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, readOnly=True),
            'user': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                ref='#/definitions/User'
            ),
            'medical_license': openapi.Schema(type=openapi.TYPE_STRING),
            'specialization': openapi.Schema(type=openapi.TYPE_STRING),
            'hospital': openapi.Schema(type=openapi.TYPE_STRING),
            'years_of_experience': openapi.Schema(type=openapi.TYPE_INTEGER),
            'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    ),
    'MedicalRecord': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, readOnly=True),
            'patient': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                ref='#/definitions/Patient'
            ),
            'created_by': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                ref='#/definitions/Doctor'
            ),
            'date': openapi.Schema(
                type=openapi.TYPE_STRING,
                format='date-time'
            ),
            'record_type': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=[
                    'consultation', 'prescription', 'test', 
                    'vaccination', 'surgery', 'hospitalization', 'other'
                ]
            ),
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'diagnosis': openapi.Schema(type=openapi.TYPE_STRING),
            'prescription': openapi.Schema(type=openapi.TYPE_STRING),
            'notes': openapi.Schema(type=openapi.TYPE_STRING),
            'file': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
            'is_emergency': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    ),
    'MedicalTest': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, readOnly=True),
            'record': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                ref='#/definitions/MedicalRecord'
            ),
            'test_name': openapi.Schema(type=openapi.TYPE_STRING),
            'test_date': openapi.Schema(
                type=openapi.TYPE_STRING,
                format='date'
            ),
            'result': openapi.Schema(type=openapi.TYPE_STRING),
            'unit': openapi.Schema(type=openapi.TYPE_STRING),
            'normal_range': openapi.Schema(type=openapi.TYPE_STRING),
            'lab_name': openapi.Schema(type=openapi.TYPE_STRING),
            'file': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
        }
    ),
}

# Configuration OpenAPI
INFO = openapi.Info(
    title="API TOHPITOH - Carnet Médical",
    default_version="v1",
    description="""
    # 🩺 API TOHPITOH - Système de Gestion de Carnet Médical
    
    ## 📋 Description
    API REST complète pour la gestion des carnets médicaux numériques.
    
    ## 👥 Rôles d'utilisateur
    - **Patient** : Peut consulter et télécharger ses propres dossiers
    - **Docteur** : Peut créer, modifier et consulter les dossiers de ses patients
    - **Administrateur** : Gestion complète du système
    
    ## 🔐 Authentification
    L'API utilise JWT (JSON Web Tokens) pour l'authentification.
    Incluez le token dans le header: `Authorization: Bearer {token}`
    
    ## 📊 Endpoints principaux
    1. **/api/auth/** - Authentification et gestion des utilisateurs
    2. **/api/medical-records/** - Dossiers médicaux
    3. **/api/patients/** - Profils patients
    4. **/api/doctors/** - Profils médecins
    5. **/api/pdf/** - Génération de PDF
    
    ## 🔗 Liens utiles
    - [Interface Swagger](/swagger/)
    - [Documentation ReDoc](/redoc/)
    - [Interface d'administration](/admin/)
    
    ## 📞 Support
    Pour le support technique, contactez: support@tohpitoh.com
    """,
    terms_of_service="https://tohpitoh.com/terms/",
    contact=openapi.Contact(
        email="support@tohpitoh.com",
        name="Support TOHPITOH",
        url="https://tohpitoh.com/contact"
    ),
    license=openapi.License(
        name="License Propriétaire",
        url="https://tohpitoh.com/license"
    ),
)

# Configurations supplémentaires
EXTERNAL_DOCS = {
    "description": "Documentation complète",
    "url": "https://docs.tohpitoh.com"
}
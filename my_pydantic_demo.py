"""
Fichier: pydantic_demmo.py
Description: Tutoriel complet Pydantic avec erreurs et corrections
"""

# ==================== ERREUR 1: IMPORTATION ====================
# ❌ MAUVAIS (conflit de noms si le fichier s'appelle pydantic.py)
# from pydantic import BaseModel

# ✅ CORRECTION (changer le nom du fichier en pydantic_demo.py)
from pydantic import BaseModel, EmailStr, field_validator, Field, ValidationError
from typing import Optional, List
import json

# ==================== ERREUR 2: MODÈLE DE BASE ====================
# ❌ MAUVAIS (pas d'héritage de BaseModel)
# class User:
#     name: str
#     age: int

# ✅ CORRECTION
class User(BaseModel):
    """Modèle utilisateur de base"""
    name: str
    age: int

# Test
try:
    user = User(name="Alice", age=25)  # ✅ Valide
    # user = User(name="Bob", age="25")  # ❌ Lève ValidationError
except ValidationError as e:
    print("Erreur de validation:", e.json())

# ==================== ERREUR 3: VALIDATION EMAIL ====================
# ❌ MAUVAIS (validation email manquante)
# class UserEmail:
#     email: str

# ✅ CORRECTION
class UserEmail(BaseModel):
    """Validation d'email avec EmailStr"""
    email: EmailStr  # Nécessite pip install pydantic[email]

# Test
try:
    email_user = UserEmail(email="alice@example.com")  # ✅ Valide
    # email_user = UserEmail(email="invalid")  # ❌ Erreur
except ValidationError as e:
    print("Erreur email:", e.json())

# ==================== ERREUR 4: VALIDATION PERSONNALISÉE ====================
# ❌ MAUVAIS (mauvaise syntaxe de validateur)
# class UserAge:
#     age: int
#     
#     def validate_age(age):
#         if age < 18:
#             raise ValueError("Trop jeune")

# ✅ CORRECTION
class UserAge(BaseModel):
    age: int

    @field_validator('age')
    def validate_age(cls, value):
        """Validation personnalisée pour l'âge"""
        if value < 18:
            raise ValueError("L'âge doit être ≥ 18")
        return value

# Test
try:
    age_user = UserAge(age=20)  # ✅ Valide
    # age_user = UserAge(age=15)  # ❌ Erreur
except ValidationError as e:
    print("Erreur âge:", e.json())

# ==================== ERREUR 5: SÉRIALISATION JSON ====================
# ❌ MAUVAIS (ancienne méthode)
# json_data = user.json()

# ✅ CORRECTION (Pydantic v2)
user = User(name="Alice", age=25)
json_data = user.model_dump_json()  # Sérialisation
print("JSON:", json_data)

# Désérialisation
user_from_json = User.model_validate_json(json_data)
print("Depuis JSON:", user_from_json)

# ==================== ERREUR 6: CHAMPS OPTIONNELS ====================
# ❌ MAUVAIS (sans Optional)
# class UserOptional:
#     name: str
#     age: int = None

# ✅ CORRECTION
class UserOptional(BaseModel):
    name: str
    age: Optional[int] = None  # Champ optionnel

# Test
optional_user = UserOptional(name="Bob")  # ✅ age=None par défaut
print("Utilisateur optionnel:", optional_user)

# ==================== ERREUR 7: MODÈLES IMBRIQUÉS ====================
class Address(BaseModel):
    street: str
    city: str

class CompanyUser(BaseModel):
    user: User
    address: Address

# Test
company_user = CompanyUser(
    user={"name": "Alice", "age": 30},
    address={"street": "123 Main", "city": "Paris"}
)
print("Utilisateur avec adresse:", company_user)

"""
=== GUIDE DES ERREURS COURANTES ===
1. Conflit de noms: Ne pas nommer le fichier pydantic.py
2. Oublier BaseModel: Toujours hériter de BaseModel
3. EmailStr: Pour les emails, utiliser EmailStr
4. Validateurs: Toujours utiliser @field_validator
5. JSON: Utiliser model_dump_json() au lieu de .json()
6. Champs optionnels: Utiliser Optional[type] = None
"""

# ==================== BONUS: DATACLASS VS PYDANTIC ====================
from dataclasses import dataclass

@dataclass
class UserDataclass:
    name: str
    age: int

# Test (aucune validation automatique)
dc_user = UserDataclass(name="Alice", age="25")  # ❌ Problème mais pas d'erreur
print("Dataclass (non validé):", dc_user)
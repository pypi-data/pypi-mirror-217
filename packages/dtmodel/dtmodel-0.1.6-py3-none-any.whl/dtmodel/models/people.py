__all__ = [
        'Person',
        'Doctor',
        'Therapist',
        'Employee',
        'User',
        'Patient'
]

from dtmodel.base._imports import *
from dtmodel.model import context_model
import bcrypt
from dtmodel.models.bases import *
from ..functions import *

@context_model
@descdataclass
class Person(SelfKey, PersonCode, GenderIdentity, CPF, PersonBase):
    EXIST_PARAMS = ['code', 'cpf']
    SINGULAR = 'Pessoa'
    
    @property
    def  age(self):
        return years(self.bdate, datetime.date.today())
    
    @property
    def fullname(self):
        return f'{self.fname} {self.lname}'
    
    @property
    def social_name(self):
        return self.name
    
    @property
    def short_name(self):
        return f'{self.fname.split()[0]} {self.lname.split()[-1]}'
    
    def __str__(self):
        return self.social_name if not is_null(self.social_name) else self.fullname



@context_model
@descdataclass
class Patient(SelfKey, Address, Email, Phone,  Profile):
    EXIST_PARAMS = 'person_key'
    SINGULAR = 'Paciente'

    def __str__(self):
        return self.person.__str__()
    
    def __lt__(self, other):
        return normalize_lower(str(self)) < normalize_lower(str(other))
    
    
@descdataclass
class Provider(SelfKey, Address, Email, Phone, Register, Profile):

    def __str__(self):
        return '{} {}'.format('Dr.' if self.person.gender.name == 'M' else 'Dra.', self.person.short_name)


@context_model
@descdataclass
class Doctor(Provider):
    EXIST_PARAMS = 'person_key'
    SINGULAR = 'Médico'


@context_model
@descdataclass
class Therapist(Provider):
    EXIST_PARAMS = 'person_key'
    SINGULAR = 'Terapeuta'


@context_model
@descdataclass
class Employee(SelfKey, WorkActivity, Address, Email, Phone, Salary, PersonKey):
    EXIST_PARAMS = 'person_key'
    SINGULAR = 'Funcionário'


@context_model
@descdataclass
class User(SelfKey, PasswordRepeat, Password, ProfileKey, Username):
    EXIST_PARAMS = ['username', 'profile_key']
    SINGULAR = 'Usuário'

    
    def __post_init__(self, password_repeat: bytes = None):
        if not is_null(password_repeat):
            if isinstance(password_repeat, str):
                password_repeat = password_repeat.encode('utf-8')
                assert self.password == password_repeat
                self.password = bcrypt.hashpw(self.password, bcrypt.gensalt())
        
        
    
from __future__ import annotations

__all__ = [
        'Register',
        'PersonCode',
        'PersonKey',
        'PersonBase',
        'Salary',
        'WorkActivity',
        'Username',
        'Password',
        'PasswordRepeat',
        'ProfileKey',
        'PatientKey',
        'Creator',
        'RequiredCreator',
        'Age',
        'SocialName',
        'ProviderKey',
        'TherapistKey',
        'DoctorKey',
        'Profile',
        'CPF',
        'GenderIdentity'
]
from dtmodel.base import *
from dtmodel.descriptor import *
from dtmodel.models.enums import *

def person_code(self):
    return '{}{}{}{}'.format(
            self.gender.name,
            re.sub(r'-', '', str(self.bdate)),
            self.fname[:2].upper(),
            self.lname.split()[-1][:2].upper()
    )


@dataclass
class Register:
    register: str = StringValidator(label='registro')
    

@dataclass
class Age:
    age: float = FloatValidator(default=None, label='idade')


@dataclass
class PersonCode:
    code: str = NoFormValidator(default=None, update_auto=person_code, label='código da pessoa')


@dataclass
class PersonKey:
    person_key: Key = KeyValidator(item_name='person', table='Person', label='pessoa')
    
    @property
    def age(self):
        return self.person.age
    
    @property
    def fullname(self):
        return self.person.fullname
    
    @property
    def social_name(self):
        return self.person.social_name
    
    @property
    def bdate(self):
        return self.person.bdate


@dataclass
class PatientKey:
    patient_key: Key = KeyValidator(item_name='patient', table='Patient', label='paciente')

@dataclass
class DoctorKey:
    doctor_key: Key = KeyValidator(item_name='doctor', table='Doctor', label='médico')
    
    
@dataclass
class TherapistKey:
    therapist_key: Key = KeyValidator(item_name='therapist', table='Therapist', label='terapeuta')


@dataclass
class Creator:
    creator: str = KeyValidator(item_name='user', table='User', default='zjhm79ltaw87', label='usuário criador')
    
@dataclass
class CPF:
    cpf: str = StringValidator(default=None, label='CPF', field_size='col-sm-12 col-md-12 col-lg-3')


@dataclass
class RequiredCreator:
    creator: Key = KeyValidator(item_name='user', table='User', label='usuário criador')


@dataclass
class PersonBase:
    fname: str = StringValidator(label='primeiro nome', field_size='col-sm-12 col-md-6 col-lg-2')
    lname: str = StringValidator(label='sobrenome', field_size='col-sm-12 col-md-6 col-lg-3')
    bdate: datetime.date = DateValidator(compare=False, label='data de nascimento', field_size='col-sm-12 col-md-6 col-lg-2')
    gender: Gender = EnumValidator(compare=False, label='gênero ao nascer', field_size='col-sm-12 col-md-6 col-lg-2')


@dataclass
class GenderIdentity:
    name: str = StringValidator(default=None, compare=False, label='nome social', field_size='col-sm-12 col-md-4')
    transgender: str = CheckboxValidator(default=False, label='transgênero', field_size='col-sm-12 col-md-4')
    non_binary: str = CheckboxValidator(default=False, label='não binário', field_size='col-sm-12 col-md-4')


@dataclass
class Salary:
    scope: EmployeeScope = Validator()
    base_value: Decimal = Validator(min=Decimal('0.0'), default=1)
    salary_indexed: bool = Validator(default=True)
    active: bool = Validator(default=True)
    
    
@dataclass
class WorkActivity:
    hours_day: float = Validator(min=0, max=24, default=8)
    days_month: float = Validator(min=0, max=31, default=22)
    telephonist: bool = Validator(default=True)
    housekeeping: bool = Validator(default=True)
    external: bool = Validator(default=True)
    manager: bool = Validator(default=True)
    financial: bool = Validator(default=True)
    assistant: bool = Validator(default=True)
    
    
@dataclass
class SocialName:
    name: str = Validator(default=None, label='Nome Social', compare=False)


@dataclass
class Username:
    username: str = Validator(min_lenght=5)
    
    
@dataclass
class Password:
    password: bytes = Validator(min_lenght=5, private=True)
    

@dataclass
class PasswordRepeat:
    password_repeat: InitVar[bytes] = None
    

@dataclass
class ProfileKey:
    profile_key: TableKey = Validator(tables=['Patient', 'Doctor', 'Therapist', 'Employee'], item_name='profile')


@dataclass
class ProviderKey:
    provider_key: TableKey = Validator(tables=['Doctor', 'Therapist'], item_name='provider')


@dataclass
class Profile(PersonKey):
    EXIST_PARAMS: ClassVar[ExistParams] = 'person_key'

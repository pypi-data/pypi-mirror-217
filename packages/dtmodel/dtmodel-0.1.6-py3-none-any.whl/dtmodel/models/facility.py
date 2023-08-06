__all__ = [
        'Facility',
        'Invoice',
        'Service',
        'Expense'
]

from dtmodel.base._imports import *

from dtmodel.descriptor import *
from dtmodel.functions import *
from dtmodel.model import *
from dtmodel.models.bases import *


@context_model
@descdataclass
class Facility(SelfKey, Email, Phone, Address, RequiredName):
    SINGULAR = 'Empresa'
    EXIST_PARAMS = 'name'


@context_model
@descdataclass
class Invoice(Search, SelfKey, Created, Creator, Description, ServiceDate, Payment, FacilityKey, ServiceKey, PatientKey):
    SINGULAR = 'Fatura'
    EXIST_PARAMS = 'patient_key payment_date payment_value payment_method'
    facility_key: str = KeyValidator(default=None, table='Facility', item_name='facility', label='empresa', no_form=True)
    
    def __post_init__(self):
        super().__post_init__()
        if not self.facility_key:
            self.facility_key = self.service.facility_key
            
    def __str__(self):
        return f'fatura {self.payment_date} de {self.service} paciente {self.patient}'


@context_model
@descdataclass
class Expense(Search, SelfKey, Created, Creator, Payment, FacilityKey):
    SINGULAR = 'Despesa'
    EXIST_PARAMS = 'facility_key payment_date payment_value payment_method'


@context_model
@descdataclass
class Service(Search, SelfKey, Created, Creator, Description, Active, OptionalName, FacilityKey, Percentage, Price, ServiceTypeBase):
    SINGULAR = 'Serviço'
    DETA_QUERY = {'active': True}
    EXIST_PARAMS = 'type therapist_key doctor_key price'

    therapist_key: str = Validator(default=None, table='Therapist', item_name='provider')
    doctor_key: str = Validator(default=None, table='Doctor', item_name='provider')
    
    def __post_init__(self):
        if not self.price:
            self.price = Decimal('0.0')
        assert self.therapist_key or self.doctor_key
        super().__post_init__()
    
    def __str__(self):
        return f'{self.provider} {self.type.value} R$ {self.price}'
    
    def __lt__(self, other):
        try:
            return (self.provider.person.short_name, self.price) < (other.provider.person.short_name, other.price)
        except TypeError:
            return False
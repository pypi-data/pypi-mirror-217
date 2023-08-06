__all__ = [
        'MainComplaint',
        'SOAP',
        'Intro',
        'TreatmentResponse',
        'VisitContext',
        'MedicationKey',
        'Recipe',
        'MedicationPackage',
        'DosageForm',
        'ActiveSet',
        'Dosage',
        'VisitType',
        'CIDs',
        'Subjective',
        'Objective',
        'Assessment',
        'Plan',
        'Complement',
        'Pharmaceutical'
]

from dtmodel.descriptor import Validator
from dtmodel.functions import *
from dtmodel.models.enums import *
from dtmodel.base import *
from dtmodel.descriptor import *

@dataclass
class MedicationKey:
    medication_key: Key = KeyValidator(table='Medication', item_name='medication', label='medicação')
    
    
@dataclass
class ActiveSet:
    
    class ActiveSetString(UserString):
        
        class Active(UserString):
            def __init__(self, value: str):
                self.name, self.value, self.unit = [
                        remove_extra_whitespaces(i) for i in re.split(r'\s(\d+[.,]\d+|\d+)', value)]
                super().__init__(remove_extra_whitespaces(value))
            
            def __repr__(self):
                return f'Active(name="{self.name}", value={self.value}, unit="{self.unit}")'
        
        def __init__(self, value: str):
            self.sets = list()
            for i in filter(lambda x: x != '', re.split(r'\+', value)):
                self.sets.append(self.Active(i))
            super().__init__(remove_extra_whitespaces(value))
        
        @property
        def actives(self):
            return self.sets
        
        def __repr__(self):
            return f'{self.actives!r}'
        
    active_set: ActiveSetString = StringValidator(label='princípios ativos', search=True)
    
    @property
    def actives(self):
        return self.active_set.actives
    
    @property
    def active_names(self):
        return tuple([i.name for i in self.actives])
    
    @property
    def active_values(self):
        return tuple([f'{i.value}{i.unit}' for i in self.actives])


@dataclass
class DosageForm:
    
    class DosageFormEnum(BaseEnum):
        U = 'unidade'
        GT = 'gota'
        MC = 'microgota'
        ML = 'ml'
        AMP = 'ampola'
    
    dosage_form: DosageFormEnum = EnumValidator(default='U', label='forma de dosagem', search=True)
    

@dataclass
class Recipe:
    
    class RecipeEnum(BaseEnum):
        A1 = 'A1'
        B1 = 'B1'
        B2 = 'B2'
        C1 = 'C1'
        C2 = 'C2'
        C3 = 'C3'
        S0 = 'S0'
        S1 = 'S1'
        
    recipe: RecipeEnum = EnumValidator(default='C3', label='receita', search=True)
    
    
@dataclass
class MedicationPackage:
    
    class Package(UserString):
        def __init__(self, value: str):
            self.value, self.unit = [remove_extra_whitespaces(i) for i in re.split(r'(\d+[.,]\d+|\d+)\s', value) if i]
            if self.value:
                if re.match(r'[.,]', self.value):
                    self.value = float(self.value)
                else:
                    self.value = int(self.value)
            super().__init__(value)
        
        def __repr__(self):
            return 'Package(value={}, unit="{}")'.format(self.value, self.unit)
        
    package: Package = StringValidator(default='30 cp', label='conteúdo do pacote', search=True)
    
    @property
    def package_content(self):
        return self.package.split(maxsplit=1)

@dataclass
class VisitType:
    type: VisitTypeEnum = EnumValidator(default='CO', label='tipo de visita', field_size='col-sm-6 col-md-3')

@dataclass
class MainComplaint:
    main_complaint: str = StringValidator(default=None, label='queixa principal', field_size='col-sm-12 col-md-6')


@dataclass
class Intro:
    intro: str = TextValidator(default=None, repr=False, label='introdução')

@dataclass
class SOAP:
    subjective: str = TextValidator(default=None, repr=False, label='sintomas')
    objective: str = TextValidator(default=None, repr=False, label='exame médico')
    assessment: str = TextValidator(default=None, repr=False, label='análise')
    plan: str = TextValidator(default=None, repr=False, label='plano terapêutico')


@dataclass
class Subjective:
    subjective: str = TextValidator(default=None, repr=False, label='sintomas', field_size='col-sm-6 col-md-4')
    

@dataclass
class Objective:
    objective: str = TextValidator(default=None, repr=False, label='exame médico', field_size='col-sm-6 col-md-4')
    
@dataclass
class Assessment:
    assessment: str = TextValidator(default=None, repr=False, label='análise', field_size='col-sm-12 col-md-8')
    
@dataclass
class Plan:
    plan: str = TextValidator(default=None, repr=False, label='plano terapêutico', field_size='col-sm-12')

@dataclass
class TreatmentResponse:
    treatment: str = TextValidator(default=None, repr=False, label='tratamentos', field_size='col-sm-6 col-md-4')
    response: str = TextValidator(default=None, repr=False, label='resposta terapêutica', field_size='col-sm-6 col-md-4')


@dataclass
class CIDs:
    cids: str = TextValidator(default=None, label='diagnóstico', field_size='col-md-4')


@dataclass
class VisitContext:
    context: str = TextValidator(default=None, repr=False, label='contexto de vida atual', field_size='col-sm-6 col-md-4')


@dataclass
class Complement:
    complement: str = TextValidator(default=None, repr=False, label='comorbidades', field_size='col-sm-6 col-md-4')


@dataclass
class Dosage:
    
    class DosageString(UserString):
        NUMBER = re.compile(r'(\d+[.,]\d+|\d+)')
        
        def __init__(self, value: str):
            self.digit = self.dosage_digit(value)
            self.number = self.dosage_number(self.digit)
            self.unit = self.dosage_unit(value)
            super().__init__(value)
            
        @classmethod
        def dosage_unit(cls, value):
            split = [i for i in cls.NUMBER.split(remove_extra_whitespaces(value)) if i]
            if len(split) > 1:
                return ' '.join(split[1:])
            return None
            
        @classmethod
        def dosage_digit(cls, value: str) -> Optional[str]:
            match = cls.NUMBER.match(value)
            if match:
                return match.group()
            return None
        
        @staticmethod
        def dosage_number(value: str) -> Optional[float]:
            if value:
                return float(re.sub(r',', '.', value))
            return None
            
    dosage: DosageString = StringValidator(default='1 un', label='dosagem')
    
    @property
    def unit(self):
        return self.dosage.unit
    

        
@dataclass
class Pharmaceutical:
    pharmaceutical: str = StringValidator(default=None, label='indústria farmacêutica')





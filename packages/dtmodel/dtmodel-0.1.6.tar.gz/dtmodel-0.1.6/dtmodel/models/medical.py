__all__ = [
        'MedicalVisit',
        'Event',
        'Medication',
        'Prescription'
]

from dtmodel.base._imports import *
from dtmodel.descriptor import Validator
from dtmodel.model import context_model
from dtmodel.parse import Parser
from dtmodel.models.bases import *
from dtmodel.functions import *
from dtmodel.regex import *
from dtmodel.descriptor import *


@context_model
@descdataclass
class MedicalVisit(SelfKey, Creator, End, Plan, CIDs, Assessment, TreatmentResponse, Complement, VisitContext, Objective, Subjective, Intro, MainComplaint, Start, Date, VisitType, PatientKey):
    EXIST_PARAMS = 'patient_key date main_complaint'
    SINGULAR = 'Visita Médica'
    PLURAL = 'Visitas Médicas'
    creator: str = KeyValidator(default='zjhm79ltaw87', table='User', item_name='user')
    next: int = IntValidator(default=60, label='dias para próxima visita', field_size='col-sm-4')
    start: datetime.datetime = DatetimeValidator(default_factory=local_now, label='início', field_size='col-sm-6 col-md-3')
    date: datetime.date = DateValidator(default_factory=local_today, label='data', field_size='d-none')
    end: datetime.datetime = DatetimeValidator(post_init_factory=local_now, label='final', field_size='col-sm-4')

    
    def __post_init__(self):
        super().__post_init__()
        # if all([self.start, self.end]):
        #     if (self.end.toordinal() - self.start.toordinal()) > 2/24/60/60:
        #         self.end = self.start + datetime.timedelta(hours=2)
    
    @property
    def next_visit(self):
        return self.start.date() + datetime.timedelta(days=self.next or 60)




@context_model
@descdataclass
class Medication(Search, SelfKey, Recipe, DosageForm, MedicationPackage, Pharmaceutical, OptionalName, ActiveSet):
    """
    Attributes
    ----------
    active_set: str
        names of active sets separated by "+" if more than one; each one should always be composed by
        "name", "value", and "unit"
    name: Optional[str]
        the name of the medication, if not generic
    dosage_form: Optional[str] = "U"
        the dosage form of the medication; if unit (as "U", the default) it will assume the value of package unit;
        it can be drops ("D") or microdrops ("MD"), ml ("ML"), g ("G")
    package: Optional[str] = "30 cp"
        a string with "" and "" separated by space

    """
    
    SINGULAR = 'Medicação'
    PLURAL = 'Medicações'
    ITEM_NAME = 'medication'
    EXIST_PARAMS = 'active_set name package'
    
    
    def __str__(self):
        return '{} {}'.format(self.simple_name, self.package)
    
    @property
    def generic(self):
        return is_null(self.name)
    
    @property
    def simple_name(self):
        if self.generic:
            return self.generic_name
        return self.branded_name
    
    @property
    def generic_name(self):
        return ' + '.join([f'{i.name.title()} {i.value}{i.unit}' for i in self.actives])
    
    @property
    def branded_name(self):
        return '{} ({}) {}'.format(
                self.name,
                '/'.join(self.active_names),
                '+'.join(self.active_values)
        )

@context_model
@descdataclass
class Prescription(SelfKey, EndDate, Notes, Days, Interval, Dosage, StartDate, MedicationKey, PatientKey):
    SINGULAR = 'Prescrição'
    PLURAL = 'Prescrições'
    ITEM_NAME = 'prescription'
    EXIST_PARAMS = 'patient_key medication_key'
    
    active: bool = CheckboxValidator(default=True, label='ativo')
    end: datetime.date = DateValidator(default=None, no_form=True, label='final')
    
    
    @property
    def unit(self):
        return self.dosage.unit or self.medication.dosage_form.value if not self.medication.dosage_form.name == 'U' \
            else self.medication.package.unit
    
    @property
    def dosage_number(self):
        return self.dosage.number
    

    def __str__(self):
        return '{} {} {} {}. {}'.format(self.medication, self.dosage_number, self.unit, self.interval, self.notes)
    
    def __post_init__(self):
        super().__post_init__()
        if self.active is False:
            if not self.end:
                self.end = local_today()



@context_model
@descdataclass
class Event(SelfKey, Creator, RequiredName, PatientKey):
    EXIST_PARAMS = 'patient_key age name'
    SINGULAR = 'Evento Vital'
    PLURAL = 'Eventos Vitais'
    ITEM_NAME = 'event'
    name: str = StringValidator(label='evento', field_size='col-sm-12 col-md-9')
    when: str = StringValidator(auto=lambda x: x.patient.age, db=False, label='idade ou data', field_size='col-sm-12 col-md-3')
    age: float = NoFormValidator(default=None, auto=lambda x: x.event_age())
    
    def __lt__(self, other):
        if all([not is_null(self.age), not is_null(other.age)]):
            return self.age < other.age
        return False
    
    def __str__(self):
        return '{} anos: {}'.format(self.age, self.name)
    
    @property
    def html(self):
        return '<li class="list-group-item">{}</li>'.format(str(self))
    
    @property
    def bdate(self):
        return self.patient.person.bdate
    
    def event_age(self):
        if self.when:
            if all([isinstance(self.when, str), len(self.when) >= 1]):
                
                def try_age():
                    self.age = Parser.get(self.when, float)
                
                def try_year():
                    year = re.match(YEAR_RAW, self.when)
                    print(year)
                    if year:
                        self.age = years(self.bdate, datetime.date(int(year.group()), self.bdate.month, self.bdate.day))
                    else:
                        try_age()
                
                def try_month_year():
                    month_year = re.match(MONTH_YEAR_RAW, self.when)
                    print(month_year)
                    if month_year:
                        self.age = years(self.bdate, datetime.date(int(month_year.group(2)), int(month_year.group(1)),
                                                                   self.bdate.day))
                    else:
                        try_year()
                
                def try_day_month_year():
                    day_month_year = re.match(DAY_MONTH_YEAR_RAW, self.when)
                    print(day_month_year)
                    if day_month_year:
                        self.age = years(self.bdate,
                                         datetime.date(int(day_month_year.group(3)), int(day_month_year.group(2)),
                                                       int(day_month_year.group(1))))
                    else:
                        try_month_year()
                
                try_day_month_year()
        else:
            self.age = self.patient.age
        return self.age



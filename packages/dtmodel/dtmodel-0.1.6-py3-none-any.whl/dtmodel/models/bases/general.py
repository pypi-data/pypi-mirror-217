__all__ = [
        'Address',
        'Phone',
        'Email',
        'RequiredName',
        'OptionalName',
        'Date',
        'Created',
        'Description',
        'Active',
        'Search',
        'Price',
        'Percentage',
        'Start',
        'End',
        'Interval',
        'Days',
        'StartDate',
        'Notes',
        'EndDate'
	]
from dtmodel.base._imports import *
from dtmodel.descriptor import *
from dtmodel.base.base_enum import BaseEnum
from dtmodel.functions import *


@dataclass
class Notes:
    notes: str = TextValidator(default=None, label='anotações')

@dataclass
class Active:
    active: bool = CheckboxValidator(default=True, label='ativo')
    
    
@dataclass
class Start:
    start: datetime.datetime = DatetimeValidator(default_factory=local_now, label='início')
    
    
@dataclass
class End:
    end: datetime.datetime = DatetimeValidator(post_init_factory=local_now, label='final')
    
    
@dataclass
class Price:
    price: Decimal = NumberValidator(default=Decimal('0.0'), label='preço', step=0.01, min=0)
    
    
@dataclass
class Address:
    address: str = TextValidator(default_factory=str, repr=False, compare=False, label='endereço')
    city: str = StringValidator(default_factory=str, compare=False, label='cidade/estado')
    
    
@dataclass
class Phone:
    phone: str = StringValidator(default_factory=str, compare=False, label='telefone', field_size='col-sm-6')
    
    
@dataclass
class Description:
    description: str = TextValidator(default=None, compare=False, repr=False, label='descrição')


@dataclass
class Email:
    email: str = StringValidator(default_factory=str, compare=False, label='email', field_size='col-sm-6')
    
    
@dataclass
class RequiredName:
    name: str = StringValidator(label='nome')
    
    
@dataclass
class OptionalName:
    name: str = StringValidator(default=None, label='nome')
    
    
@dataclass
class Percentage:
    percentage: float = FloatValidator(default=None, min=0.0, max=100.0, step=0.01, label='porcentagem')
    
    
@dataclass
class Date:
    date: datetime.date = DateValidator(default_factory=datetime.date.today, compare=True, label='data')
    
    @property
    def past_days(self):
        return days(self.date)
    
    @property
    def past_months(self):
        return months(self.date)
    
    @property
    def past_years(self):
        return months(self.date)
    
    
@dataclass
class Created:
    created: datetime.datetime = NoFormValidator(post_init_factory=datetime.date.today, repr=False, label='data de criação')
    
    def __lt__(self, other):
        return self.created.date() < other.created.date()
    
    @property
    def past_days(self):
        return days(self.created.date())
    
    @property
    def past_months(self):
        return months(self.created.date())
    
    @property
    def past_years(self):
        return years(self.created.date())
    
    
@dataclass
class Search:
    search: str = SearchValidator(default=None, auto=lambda self: normalize_lower(str(self)), repr=False, label='busca')


@dataclass
class Interval:
    
    class IntervalEnum(BaseEnum):
        _ignore_ = 'IntervalEnum h'
        IntervalEnum = vars()
        for h in range(1, 25):
            IntervalEnum[f'H{h}'] = 'a cada {} {}'.format(h, 'hora' if h == 1 else 'horas')
        F = 'ao acordar em jejum'
        B = 'após o café'
        M = 'pela manhã'
        L = 'após o almoço'
        D = 'após o jantar'
        N = 'ao deitar'
        for h in range(1, 91):
            IntervalEnum[f'D{h}'] = 'a cada {} {}'.format(h, 'dia' if h == 1 else 'dias')
            
    interval: IntervalEnum = EnumValidator(default='D1', label='intervalo')


@dataclass
class Days:
    
    class DaysEnum(BaseEnum):
        _ignore_ = 'DaysEnum d'
        DaysEnum = vars()
        for d in range(1, 365):
            DaysEnum[f'D{d}'] = '{} {}'.format(d, 'dia' if d == 1 else 'dias')
    
    days: DaysEnum = EnumValidator(default='D60', label='duração em dias')
    
    
@dataclass
class StartDate:
    start: datetime.date = DateValidator(default_factory=local_today, label='início')


@dataclass
class EndDate:
    end: datetime.date = DateValidator(default_factory=local_today, label='final')
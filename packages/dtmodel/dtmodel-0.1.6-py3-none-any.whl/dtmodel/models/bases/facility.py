__all__ = [
        'FacilityKey',
        'ServiceKey',
        'ServiceTypeBase',
        'Payment',
        'ServiceDate',
]
from dtmodel.base import *
from dtmodel.descriptor import *
from dtmodel.models.enums import *

@dataclass
class FacilityKey:
    facility_key: Key = KeyValidator(compare=False, label='empresa', table='Facility', item_name='facility', default=None)
    
    
@dataclass
class ServiceKey:
    service_key: Key = KeyValidator(compare=False, label='serviço', table='Service', item_name='service')


@dataclass
class ServiceDate:
    service_date: datetime.date = DateValidator(default_factory=datetime.date.today, label='data do serviço')


@dataclass
class ServiceTypeBase:
    type: ServiceType = EnumValidator(hash=True, label='tipo de serviço')


@dataclass
class Payment:
    payment_method: PaymentMethod = EnumValidator(default='CA', label='método de pagamento', field_size='col-sm-12 col-md-4')
    payment_value: Decimal = NumberValidator(default=Decimal('0.0'), label='valor do pagamento', step=0.01, min=0, field_size='col-sm-12 col-md-4')
    payment_date: datetime.date = DateValidator(default_factory=datetime.date.today, label='data de pagamento', field_size='col-sm-12 col-md-4')
    
    @classmethod
    async def total_payment(cls):
        return float(sum([Decimal(i.get('payment_value')) for i in await cls.fetch_all()])).__round__(2)
    
    
    @classmethod
    async def date_payment(cls, year: int, month: int, day: int, facility_key: str = 'pfz7cc10laiu'):
        return float(sum([Decimal(i.get('payment_value')) for i in
                          await cls.fetch_all({
                                  'payment_date': str(datetime.date(year, month, day)),
                                  'facility_key': facility_key
                          })])).__round__(2)
    
    @classmethod
    async def month_payment(cls, year: int, month: int, facility_key: str = 'pfz7cc10laiu'):
        return float(sum([Decimal(i.get('payment_value')) for i in await cls.fetch_all(
                {
                        'payment_date?contains': str(datetime.date(year, month, 1))[:8],
                        'facility_key': facility_key
                    
                })])).__round__(2)
    
    @classmethod
    async def year_payment(cls, year: int, facility_key: str = 'pfz7cc10laiu'):
        return float(sum([Decimal(i.get('payment_value')) for i in
                          await cls.fetch_all({
                                  'payment_date?contains': str(year),
                                  'facility_key': facility_key
                          })])).__round__(2)
    
    @staticmethod
    async def liquid_income(year: int, month: int):
        invoices = await ModelMap['Invoice'].month_payment(year, month)
        expenses = await ModelMap['Expense'].month_payment(year, month)
        return float(invoices - expenses).__round__(2)



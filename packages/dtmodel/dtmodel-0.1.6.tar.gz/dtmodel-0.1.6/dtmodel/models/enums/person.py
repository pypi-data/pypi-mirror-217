__all__ = [
        'Gender',
        'EmployeeScope'
]

from dtmodel.base.base_enum import BaseEnum

class Gender(BaseEnum):
    M = 'Masculino'
    F = 'Feminino'
    

class EmployeeScope(BaseEnum):
    DIA = 'Diarista'
    CLT = 'CLT'
    SOC = 'Sócio Proprietário'
    TER = 'Terceirizado'
    EST = 'Estagiário'
    
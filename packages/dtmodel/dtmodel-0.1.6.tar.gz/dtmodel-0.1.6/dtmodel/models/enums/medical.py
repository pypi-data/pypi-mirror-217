__all__ = [
        'VisitTypeEnum',
]

from dtmodel.base.base_enum import BaseEnum



class VisitTypeEnum(BaseEnum):
    CI = 'Inicial'
    CO = 'Seguimento'
    CE = 'Encaixe'
    CC = 'Cortesia'
    CP = 'Breve'
    RT = 'Retorno'
    VH = 'Hospitalar'
    VD = 'Domiciliar'
    RV = 'Revisão'
    

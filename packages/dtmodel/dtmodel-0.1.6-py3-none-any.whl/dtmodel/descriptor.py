__all__ = [
        'Descriptor',
        'Validator',
        'FloatValidator',
        'NumberValidator',
        'RangeValidator',
        'TextValidator',
        'IntValidator',
        'CheckboxValidator',
        'KeyValidator',
        'EnumValidator',
        'StringValidator',
        'DatetimeValidator',
        'DateValidator',
        'NoFormValidator',
        'SearchValidator'
]

from functools import partial as funcpartial
from dtmodel.base import BaseDescriptor, BaseValidator

class Descriptor(BaseDescriptor):
    pass


class Validator(BaseValidator):
    pass


class NoFormValidator(BaseValidator):
    @property
    def input_type(self):
        return None
    
    @property
    def form_field(self):
        return None


class NumberValidator(Validator):
    @property
    def input_type(self):
        return 'number'
    
    @property
    def step(self):
        return self._step or 1
    
    @property
    def min(self):
        return self._min or 0


class IntValidator(Validator):
    @property
    def input_type(self):
        return 'number'
    
    @property
    def step(self):
        return 1
    
    @property
    def min(self):
        return self._min or 0

class FloatValidator(NumberValidator):
    @property
    def step(self):
        return self._step or 0.01

    
    
class RangeValidator(NumberValidator):
    pass


class CheckboxValidator(Validator):
    @property
    def input_type(self):
        return 'checkbox'
    
    
class TextValidator(Validator):
    def __init__(self, *args, **kwargs):
        self.height = kwargs.pop('height', '100px')
        super().__init__(*args, **kwargs)
        
    @property
    def input_type(self):
        return None
    @property
    def form_field(self):
        return 'textarea'


class KeyValidator(Validator):
    @property
    def input_type(self):
        return 'text'
    
    
class DateValidator(Validator):
    @property
    def input_type(self):
        return 'date'
    
    
class DatetimeValidator(Validator):
    @property
    def input_type(self):
        return 'datetime-local'

class StringValidator(Validator):
    @property
    def input_type(self):
        return 'text'
    

class EnumValidator(Validator):
    @property
    def form_field(self):
        return 'select'
    
    
    
class SearchValidator(NoFormValidator):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_auto = funcpartial(lambda instance: instance.search_value)
    
    
    @property
    def search(self):
        return True
    

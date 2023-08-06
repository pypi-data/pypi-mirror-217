__all__ = [
        'FormField'
]
from enum import Enum
from collections import UserString
from dtmodel.endpoint.base import TEMPLATES
from dtmodel.base import *
from markupsafe import Markup

PARTIAL_FORM_FIELD_TEMPLATES = {
        'input': 'partial/form/field/input.jj',
        'textarea': 'partial/form/field/textarea.jj',
        'select': 'partial/form/field/select.jj',
    
}


class FormField:
    def __init__(self, desc: BaseValidator):
        self.desc = desc
        
    def __html__(self):
        if self.desc.form_field:
            return TEMPLATES.get_template(PARTIAL_FORM_FIELD_TEMPLATES[self.desc.form_field]).render(desc=self.desc, default=self.desc.get_default() or "")
        return ''

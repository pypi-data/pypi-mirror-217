__all__ = [
        'SelfKey'
]

from dtmodel import dataclass
from dtmodel.descriptor import *
from dtmodel.model import Model


@dataclass
class SelfKey(Model):
    key: str = NoFormValidator(default_factory=str, frozen=True, compare=False, label='chave do objeto', hash=False)
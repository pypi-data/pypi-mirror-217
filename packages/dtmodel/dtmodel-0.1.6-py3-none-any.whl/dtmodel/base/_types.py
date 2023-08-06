__all__ = [
        'T',
        'V',
        'K',
        'TupleOfTypes',
        'Key',
        'TableKey',
        'KeyList',
        'TableKeyList',
        'Undefined',
        'Text',
        'Regex'
]

from typing import TypeVar
from collections import UserString, UserList, UserDict

T = TypeVar('T')
V = TypeVar('V')
K = TypeVar('K')

TupleOfTypes = tuple[type]

Undefined = object()

class Text(UserString):
    pass

class Key(UserString):
    pass

class TableKey(UserString):
    pass

class KeyList(UserList[Key]):
    pass

class TableKeyList(UserList[TableKey]):
    pass


class Regex(UserString):
    pass


if __name__ == '__main__':
    x = Text('teste')
    print(isinstance(x, Text))

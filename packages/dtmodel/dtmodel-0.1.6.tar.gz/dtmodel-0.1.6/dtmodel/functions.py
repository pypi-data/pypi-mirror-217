from __future__ import annotations

__all__ = [
        'years',
        'days',
        'weeks',
        'months',
        'local_today',
        'local_now',
        'hours',
        'slug',
        'normalize',
        'normalize_lower',
        'hyphen_to_underscore',
        'underscore_to_hyphen',
        'remove_extra_whitespaces',
        'underscore_text',
        'titlecase',
        'getter',
        'setter',
        'last',
        'first',
        'keyattr',
        'keyitem',
        'key',
        'cammelcase',
        'exclude_keys_from_dict',
        'get_attr_or_item',
        'make_dict_from_iterable',
        'filter_dict',
        'dict_items',
        'check',
        'simple_parse',
        'process_value',
        'process_iterable',
        'attribute_is_true',
        'extract_mapping',
        'extract_iterable',
        'get_type',
        'dict_values',
        'dict_keys',
        'apply',
        'chainvars',
        'clsname',
        'is_null',
        'not_null',
        'str_to_int',
        'str_to_float',
        'str_to_number',
        'display_properties',
        'exist_params',
        'singular',
        'plural',
        'random_string',
        'filter_dict_by_keys',
        'local_date_format'
]

import datetime
import calendar
import re
from secrets import token_hex
from dataclasses import MISSING
from functools import partial
from typing import Mapping, Iterable, Any, Callable, Optional
from collections import ChainMap, deque
from operator import attrgetter, itemgetter
from unidecode import unidecode
from dtmodel.base._types import *

first = itemgetter(0)
second = itemgetter(1)
last = itemgetter(-1)
keyattr = attrgetter('key')
keyitem = itemgetter('key')
key = lambda x: keyitem(x) if isinstance(x, dict) else keyattr(x) if hasattr(x, 'key') else None

MONTHS_MAP = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro'
}

def local_date_format(date: datetime.date):
    return '{} de {} de {}'.format(date.day, MONTHS_MAP[date.month], date.year)

def str_to_int(obj: str) -> int:
    return int(str_to_float(obj).__round__(0))

def str_to_float(obj: str) -> float:
    val = obj.strip().replace(',', '.')
    return float(val).__round__(2)
    
def str_to_number(obj: str):
    number = str_to_float(obj)
    if number == int(number):
        return int(number)
    return number
    
def is_none(obj: Any) -> bool:
    return obj is None
def is_missing(obj: Any) -> bool:
    return obj is MISSING

def is_undefined(obj: Any) -> bool:
    return obj is Undefined

def is_false(obj: Any) -> bool:
    return obj is False

def is_true(obj: Any) -> bool:
    return obj is True

def is_zero(obj: Any) -> bool:
    return obj == 0

def is_empty(obj: Any) -> bool:
    return obj in [str(), dict(), list(), set(), deque(), ChainMap(), bytes()]

def is_null(obj: Any) -> bool:
    return any([is_none(obj), is_missing(obj), is_undefined(obj), is_empty(obj)])

def not_null(obj: Any) -> bool:
    return any([is_false(obj), is_true(obj), is_zero(obj), is_null(obj) is False])
    

def clsname(obj: Any):
    return get_type(obj).__name__

def dict_values(data: Mapping[K, V]) -> tuple[V]:
    return tuple(data.values())

def chainvars(model: Any) -> ChainMap:
    return ChainMap(*[vars(i) for i in get_type(model).mro()])


def dict_keys(data: Mapping[K, V]) -> tuple[K]:
    return tuple(data.keys())


def apply(obj: T, callables: list[Callable]) -> Any:
    result = obj
    for func in callables:
        result = func(result)
    return result


def dict_items(data: Mapping[K, V]) -> list[tuple[K, V]]:
    return list(data.items())


def get_type(obj: Any):
    if isinstance(obj, type):
        return obj
    return type(obj)

def check(item: T, function: Callable[[T], bool]) -> bool:
    return function(item)


filter_not_null = partial(filter, not_null)

def simple_parse(obj: T):
    return obj


def process_iterable(
        iterable: Iterable[T],
        prepare: Callable[[Iterable[T]], Any] = simple_parse,
        condition: Callable[[T], bool] = check,
        parse: Callable[[Iterable[T]], Any] = simple_parse
):
    return parse(filter(condition, prepare(iterable)))


def process_value(
        value: T,
        prepare: Callable[[T], Any] = simple_parse,
        condition: Callable[[T], bool] = lambda x: True,
        parse: Callable[[T], Any] = simple_parse) -> Optional[Any]:
    prepared = prepare(value)
    if condition(prepared) is True:
        return parse(prepared)
    return None


def attribute_is_true(item: T, name: str) -> bool:
    return getter(item, name, False) is True


def extract_mapping(
        obj: T,
        prepare: Callable[[T], Mapping[K, V]],
        key_condition: Callable[[K], bool] = simple_parse,
        value_condition: Callable[[V], bool] = simple_parse) -> Mapping[K, V]:
    return {k: v for k, v in prepare(obj).items() if all([key_condition(k), value_condition(v)])}


def extract_iterable(
        obj: T,
        prepare: Callable[[T], Iterable[V]],
        value_condition: Callable[[V], bool] = lambda v: True) -> Iterable[V]:
    return tuple(filter(value_condition, prepare(obj)))


def exclude_keys_from_dict(data: Mapping, exclude: list[str]):
    return {k: v for k, v in data.items() if not k in exclude}


def get_attr_or_item(obj: Any, name: str = 'key'):
    if isinstance(obj, Mapping):
        return obj.get(name)
    elif hasattr(obj, name):
        return getattr(obj, 'key')
    raise AttributeError(f'O objeto "{obj}" não possuir uma chave ou attributo "{name}".')


def make_dict_from_iterable(
        iterable: Iterable[T],
        key_func: Callable[[T], str] = get_attr_or_item,
        value_func: Callable[[T], Any] = lambda x: x,
        condition: Callable[[T], bool] = lambda x: True) -> dict[str, T]:
    return {key_func(item): value_func(item) for item in iterable if condition(value_func(item)) is True}


def filter_dict_by_keys(data: Mapping, exclude: list[str] = None, only: list[str] = None):
    if exclude:
        data = {k: v if not is_null(v) else "" for k, v in data.items() if not k in exclude}
    elif only:
        data = {k: v if not is_null(v) else "" for k, v in data.items() if k in only}
    return data



def filter_dict(data: Mapping[str, T], condition: Callable[[T], bool] = not_null) -> dict[str, T]:
    return make_dict_from_iterable(dict_items(data), key_func=first, value_func=second, condition=condition)



def years(start: datetime.date, end: datetime.date = None) -> float:
    end = end or datetime.date.today()
    leapdays = calendar.leapdays(start.year, end.year)
    diff = (end - start).days - leapdays
    return (diff/365).__round__(2)

def months(start: datetime.date, end: datetime.date = None) -> float:
    end = end or datetime.date.today()
    leapdays = calendar.leapdays(start.year, end.year)
    diff = (end - start).days - leapdays
    return (diff/30).__round__(1)

def days(start: datetime.date, end: datetime.date = None) -> int:
    end = end or datetime.date.today()
    return (end - start).days
    
def weeks(start: datetime.date, end: datetime.date = None) -> float:
    end = end or datetime.date.today()
    return ((end - start).days/7).__round__(1)

def local_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3)))


def local_today() -> datetime.date:
    return local_now().date()


def hours(start: datetime.datetime, end: datetime.datetime = None) -> float:
    end = end or local_now()
    return ((end - start).days/24).__round__(1)


def setter(obj: T, **kwargs) -> T:
    for k, v in kwargs.items():
        setattr(obj, k, v)
    return obj


def getter(obj: Any, prop: str, default: Any = None) -> Any:
    k = (p for p in prop.strip().split('.') if p)
    value = getattr(obj, next(k), None)
    try:
        while True:
            value = getattr(value, next(k), None)
    finally:
        return value or default

display_properties = partial(getter, prop='DISPLAY_PROPERTIES', default=list())
exist_params = partial(getter, prop='EXIST_PARAMS')
item_name = partial(getter, prop='ITEM_NAME')
singular = partial(getter, prop='SINGULAR')
plural = partial(getter, prop='PLURAL')



def remove_extra_whitespaces(string: str) -> str:
    return re.sub(r'\s+', ' ', string.strip())


def normalize(string: str) -> str:
    return unidecode(string.strip())


def normalize_lower(string: str) -> str:
    return normalize(string).lower()


def separate_words(string: str) -> str:
    def analyse_low_up(value: str):
        result = re.search(r'([a-z][A-Z])', value)
        if result:
            mid = result.span()[0] + 1
            return analyse_low_up(value[:mid] + ' ' + value[mid:])
        return value
    
    def analyse_up_up_low(value: str):
        result = re.search(r'([A-Z][A-Z][a-z])', value)
        if result:
            mid = result.span()[-1] - 2
            return analyse_up_up_low(value[:mid] + ' ' + value[mid:])
        return value
    
    return remove_extra_whitespaces(analyse_up_up_low(analyse_low_up(string)))


def underscore_text(string: str):
    return re.sub(r'\s+|-+', '_', separate_words(string))


def slug(string: str) -> str:
    return normalize_lower(underscore_text(string))


def underscore_to_hyphen(string: str) -> str:
    return re.sub(r'_+', '-', string.strip())


def hyphen_to_underscore(string: str) -> str:
    return re.sub(r'-+', '_', string.strip())


def titlecase(string: str) -> str:
    return ' '.join([w.title() if not w.isupper() and not len(w) <= 2 else w for w in re.split(r'[\s_]', separate_words(string))])


def cammelcase(string: str) -> str:
    result = ' '.join([w.title() if not w.isupper() and not len(w) <= 2 else w for w in re.split(r'[\s_]', separate_words(string))])
    return "{}{}".format(result[0].lower(), result[1:])


def random_string(size:int = 7):
    return token_hex(7)



if __name__ == '__main__':
    class Name:
        DISPLAY_PROPERTIE = 'teste'
        
    print(display_properties(Name))

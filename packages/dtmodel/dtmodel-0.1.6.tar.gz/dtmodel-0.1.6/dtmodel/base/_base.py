from __future__ import annotations

__all__ = [
        'context',
        'ModelMap',
        'BaseModel',
        'BaseDescriptor',
        'BaseValidator',
        'compare_descriptors',
        'has_dependants_descriptors',
        'descriptorsmap',
        'compare_tuple',
        'hash_tuple',
        'hash_descriptors',
        'check_hash',
        'check_compare',
        'lesser_than',
        'orderby',
        'ordered',
        'reversed_dict',
        'db_descriptorsmap',
        'query_from_string',
        'descriptors',
        'display_items',
        'display_repr',
        'eq_function',
        'repr_func',
        'repr_truth',
        'repr_descriptors',
        'compare_truth',
        'isdescriptor',
        'public_truth',
        'hash_truth',
        'form_truth',
        'required_truth',
        'has_dependants_truth',
        'descriptor_get',
        'normalize_lower_if_string',
        'public_descriptors'
]

from dtmodel.base._imports import *
from dtmodel.base._types import *
from dtmodel.functions import *
from dtmodel.parse import *
from dtmodel.base.base_enum import BaseEnum

isdescriptor = partial(check, function=lambda T: isinstance(T, BaseDescriptor))
public_truth = partial(attribute_is_true, name='public')
compare_truth = partial(attribute_is_true, name='compare')
hash_truth = partial(attribute_is_true, name='hash')
repr_truth = partial(attribute_is_true, name='repr')
isenum_truth = partial(attribute_is_true, name='isenum')
form_truth = partial(attribute_is_true, name='form')
required_truth = partial(attribute_is_true, name='required')
has_dependants_truth = partial(attribute_is_true, name='has_dependants')

descriptorsmap = partial(extract_mapping, prepare=chainvars, value_condition=isdescriptor)

descriptors = partial(apply, callables=[get_type, descriptorsmap, dict_values])

compare_descriptors = partial(extract_iterable, prepare=descriptors, value_condition=compare_truth)
public_descriptors = partial(extract_iterable, prepare=descriptors, value_condition=public_truth)
hash_descriptors = partial(extract_iterable, prepare=descriptors, value_condition=hash_truth)
enum_descriptors = partial(extract_iterable, prepare=descriptors, value_condition=isenum_truth)
repr_descriptors = partial(extract_iterable, prepare=descriptors, value_condition=repr_truth)
has_dependants_descriptors = partial(extract_iterable, prepare=descriptors, value_condition=has_dependants_truth)

normalize_lower_if_string = partial(lambda x: x if not isinstance(x, str) else normalize_lower(x))


def descriptor_get(obj: BaseModel, desc: BaseDescriptor):
    return desc.__get__(obj)


compare_tuple = partial(process_value, parse=lambda x: tuple([descriptor_get(x, d) for d in compare_descriptors(x)]))
check_compare = partial(lambda self, other: compare_tuple(self) == compare_tuple(other))
hash_tuple = partial(process_value, parse=lambda x: tuple([d.__get__(x) for d in hash_descriptors(x)]))
hash_instance = partial(apply, callables=[hash_tuple, hash])
check_hash = partial(lambda self, other: hash_instance(self) == hash_instance(other))

reversed_dict = partial(lambda x: {k: x[k] for k in reversed(x.keys())})
lesser_than = partial(lambda self, other: compare_tuple(self) < compare_tuple(other))
greater_than = partial(lambda self, other: compare_tuple(self) > compare_tuple(other))
orderby = partial(lambda iterable, public_name: sorted(iterable, key=lambda item: normalize_lower_if_string(
        getattr(item, public_name))))
db_descriptorsmap = partial(lambda x: filter_dict(descriptorsmap(x), condition=lambda d: d.db is True))
query_from_string = partial(lambda self, query_string: filter_dict(asdict(self), condition=lambda x: is_null(x) is False))


def repr_func(self: BaseModel):
    items = (f'{d.public_name}={getattr(self, d.public_name)!r}' for d in descriptors(self) if d.public == True)
    return '{}({})'.format(clsname(self), ', '.join(items))


def display_items(self: BaseModel) -> list[tuple[str, Any]]:
    if display_properties(self):
        return [(i.split('.')[-1], getter(self, i)) for i in display_properties(self)]
    return []


def display_repr(self: BaseModel):
    items = display_items(self)
    if items:
        return ', '.join([f'{i[0]}={i[1]}' for i in items])
    return None


def eq_function(self: T, other: T) -> bool:
    return check_hash(self, other)


def ordered(iterable: list[BaseModel]):
    result = iterable
    if iterable:
        item = iterable[0]
        keys = compare_descriptors(item).keys()
        for key in reversed(keys):
            result = orderby(result, key)
    return result


class BaseDescriptor(ABC):
    BASE_NUMBER_TYPES: ClassVar[TupleOfTypes] = (int, float, Decimal)
    BASE_DATETIME_TYPES: ClassVar[TupleOfTypes] = (datetime.datetime, datetime.date)
    STRING_TYPES: ClassVar[TupleOfTypes]
    BASE_TYPES: ClassVar[TupleOfTypes] = tuple([str, *BASE_NUMBER_TYPES, *BASE_DATETIME_TYPES])
    
    def __init__(
            self,
            default: Any = MISSING,
            # callabes
            default_factory: Optional[Callable[[], Any]] = MISSING,
            post_init_factory: Optional[Callable[[], Any]] = MISSING,
            auto: Optional[Callable[[BaseModel], Any]] = MISSING,
            update_auto: Optional[Callable[[BaseModel], Any]] = MISSING,
            cls_auto: Optional[Callable[[Type[BaseModel]], Any]] = MISSING,
            post_parse: Optional[Callable[[Any], Any]] = MISSING,
            pre_parse: Optional[Callable[[Any], Any]] = MISSING,
            # bools
            private: bool = False,
            repr: bool = True,
            compare: bool = True,
            hash: Optional[bool] = None,
            frozen: Optional[bool] = None,
            db: bool = True,
            tablekey: bool = False,
            multiple: bool = False,
            search: bool = False,
            # maps
            metadata: Optional[Mapping] = None,
            # strings
            label: Optional[str] = None,
            table: Optional[str] = None,
            item_name: Optional[str] = None,
            input_type: Optional[str] = None,
            field_size: Optional[str] = 'col-sm-12',
            no_form: bool = False,
            # lists
            tables: Optional[list[str]] = None
    ):
        self._default = default
        self.private = private
        self.auto = auto
        self.update_auto = update_auto
        self.default_factory = default_factory
        self.post_init_factory = post_init_factory
        self.cls_auto = cls_auto
        self._search = search
        self._label = label
        self._repr = repr
        self.compare = compare
        self.hash = hash
        self._input_type = input_type
        self.metadata = metadata
        self.table = table
        self.tables = tables
        self.multiple = multiple
        self._item_name = item_name
        self.db = db
        self.no_form = no_form
        self._tablekey = tablekey
        self.frozen = frozen
        self.post_parse = post_parse
        self.pre_parse = pre_parse
        self.field_size = field_size
        if self.hash is True:
            assert any([self.granted is True,
                        self.required is True]), f'If "hash" is True, the attribute is "granted" or "required" need be True'
    
    def __repr__(self):
        return '{}({})'.format(
                type(self).__name__,
                ', '.join([f'{k}={getattr(self, k)!r}' for k in [
                        'field_type', 'public_name', 'required', 'owner', 'dependants', 'db'
                ]])
        )
    
    def get_default(self, instance=None):
        if instance is None:
            if self.default_factory is not MISSING:
                return self.default_factory()
            elif self.cls_auto is not MISSING:
                return self.cls_auto(self.owner)
            else:
                default = self.default
                if any([default is None, default is MISSING, default == '']):
                    return ''
                return default
        return self.__get__(instance)
        
    
    @property
    def public(self):
        return True if all([self.private == False, self.repr == True]) else False
    
    @property
    def search(self):
        return self._search
    
    @property
    def input_type(self):
        return self._input_type
    
    @property
    def istext(self):
        if isinstance(self.field_type, type):
            return issubclass(self.field_type, Text)
        return None
    
    @property
    def form_field(self):
        if self.no_form:
            return None
        if self.input_type:
            return 'input'
        elif self.isenum:
            return 'select'
        elif self.istext:
            return 'textarea'
        return None
        
    
    @property
    def has_dependants(self):
        return True if any([self.tables is not None, self.table is not None]) else False
    
    @property
    def tablekey(self):
        return all([self.has_dependants is True, any([self._tablekey is True, self.tables is not None])])
    
    @property
    def item_name(self):
        if self._item_name:
            return self._item_name
        elif self.table:
            return ModelMap.get(self.table).item_name()
        return re.sub(r'_key', '', self.public_name)
    
    @property
    def repr(self):
        if self.private:
            return False
        return self._repr
    
    @property
    def dependants(self) -> tuple[Optional[Type[BaseModel]]]:
        if self.tables:
            return tuple([ModelMap.get(item) for item in self.tables])
        elif self.table:
            return tuple([ModelMap.get(self.table)])
        return tuple()
    
    @property
    def auto_or_factory(self):
        return True if any([
                self.default_factory is not MISSING,
                self.auto is not MISSING,
                self.cls_auto is not MISSING,
                self.update_auto is not MISSING,
                self.post_init_factory is not MISSING,
        ]) else False
    
    @property
    def required(self):
        return all([self._default is MISSING, self.auto_or_factory is False])
    
    @property
    def granted(self):
        return any([is_null(self._default) is False, self.auto_or_factory is True])
    
    @property
    def default(self):
        if self._default is MISSING:
            if self.auto_or_factory is True:
                return None
        return self._default
    
    @property
    def label(self):
        return self._label or self.public_name
    
    @property
    def isenum(self):
        if isinstance(self.field_type, type):
            return issubclass(self.field_type, BaseEnum)
        return False
    
    @property
    def field_type(self):
        return get_type_hints(self.owner)[self.public_name]
    
    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'
        self.public_name = name
        self.owner: Type[BaseModel] = owner
    
    def __get__(self, instance, owner=None):
        if instance is None:
            return self.default
        if hasattr(instance, self.private_name):
            return getattr(instance, self.private_name)
        return None
    
    def __set__(self, instance, value):
        if self.frozen:
            if not is_null(value):
                value = getattr(instance, self.private_name, value)
        else:
            value = self.parse(instance, self.set_lookup(instance, value))
        self.validate(instance, value)
        setattr(instance, self.private_name, value)
        if not is_null(value):
            if self.has_dependants:
                if self.tablekey:
                    model = ModelMap.get(value.split('.')[0])
                    setattr(instance, self.item_name, model.from_tabledata(value.split('.')[-1]))
                else:
                    model = ModelMap.get(self.table)
                    setattr(instance, self.item_name, model.from_tabledata(value))
    
    def set_lookup(self, instance, value):
        if self.update_auto is not MISSING:
            value = self.update_auto(instance)
        else:
            if value is None:
                if self.auto is not MISSING:
                    value = self.auto(instance)
                elif self.cls_auto is not MISSING:
                    value = self.cls_auto(self.owner)
                if self.default_factory is not MISSING:
                    value = self.default_factory()
                
        return value
    
    def parse(self, instance, value):
        if all([not_null(value), not_null(self.pre_parse)]):
            value = self.pre_parse(value)
        value = Parser.get(value, self.field_type)
        if all([not_null(value), not_null(self.post_parse)]):
            value = self.post_parse(value)
        return value or ''
    
    def validate(self, instance, value):
        pass
    
    @property
    def name(self):
        return '{}.{}'.format(self.owner.__name__, self.public_name)
    
    @property
    def type_hint(self):
        return TypeHint(self.field_type)
    
    @property
    def expected_type(self):
        return self.type_hint.expected_type
    
    
class BaseValidator(BaseDescriptor):
    def __init__(
            self,
            step: Optional[int, float] = None,
            min: Optional[int, float] = None,
            max: Optional[int, float] = None,
            min_lenght: Optional[int] = None,
            max_lenght: Optional[int] = None,
            predicate: Optional[Callable[[BaseModel], bool]] = None,
            **kwargs):
        self._min = min
        self._max = max
        self._step = step
        self._min_lenght = min_lenght
        self._max_lenght = max_lenght
        self.predicate = predicate
        super().__init__(**kwargs)
    
    def validate_null(self, instance, value):
        if is_null(value):
            if self.required:
                raise ValueError(f'{self.name} não pode ser nulo.')
    
    def validate_type(self, instance, value):
        if not self.type_hint.check_type(value):
            raise ValueError(
                    f'{self.name} exige como tipo(s) "{self.expected_type}". O encontrado para "{value}" foi "{type(value)}".')
    
    def validate_other(self, instance, value):
        if self.field_type in self.BASE_NUMBER_TYPES:
            self.validate_min(instance, value)
            self.validate_max(instance, value)
        elif hasattr(self.field_type, '__len__'):
            self.validate_min_length(instance, value)
            self.validate_max_length(instance, value)
        self.validate_predicate(instance, value)
    
    def validate_min_length(self, instance, value):
        if self._min_lenght:
            if len(value) < self._min_lenght:
                raise ValueError(
                        f'{self.name} não pode ter tamanho menor que "{self._min_lenght}". O encontrado para "{value}" é "{len(value)}".')
    
    def validate_max_length(self, instance, value):
        if self._max_lenght:
            if len(value) > self._max_lenght:
                raise ValueError(
                        f'{self.name} não pode ter tamanho maior que "{self._max_lenght}". O encontrado para "{value}" é "{len(value)}".')
    
    def validate_min(self, instance, value):
        if self._min:
            if self._min > value:
                raise ValueError(f'{self.name} não pode ser menor que "{self._min}". O encontrado é "{value}".')
    
    def validate_max(self, instance, value):
        if self._max:
            if self._max < value:
                raise ValueError(f'{self.name} não pode ser maior que "{self._max}". O encontrado é "{value}".')
    
    def validate_predicate(self, instance, value):
        if self.predicate:
            if self.predicate(value) is False:
                raise ValueError(f'{self.name} não passou no teste de predicativo com o valor "{value}".')
    
    def validate(self, instance, value):
        self.validate_null(instance, value)
        if not is_null(value):
            self.validate_type(instance, value)
            self.validate_other(instance, value)
            
    @property
    def step(self):
        return self._step
    
    @property
    def min(self):
        return self._min
    
    @property
    def max(self):
        return self._max
    
    @property
    def min_lenght(self):
        return self._min_lenght
    
    @property
    def max_lenght(self):
        return self._max_lenght


@dataclass
class BaseModel(ABC):
    SINGULAR: ClassVar[str] = None
    PLURAL: ClassVar[str] = None
    ITEM_NAME: ClassVar[str] = None
    TABLE: ClassVar[str] = None
    DISPLAY_PROPERTIES: ClassVar[tuple[str]] = None
    
    @classmethod
    def search_descriptors(cls) -> tuple[BaseDescriptor]:
        return tuple([d for d in cls.descriptors() if d.search])
    
    @property
    def search_value(self):
        if len(self.search_descriptors()) > 0:
            return normalize_lower('; '.join([str(d.__get__(self)) for d in self.search_descriptors() if not_null(d.__get__(self))]))
        return normalize_lower(str(self))
    
    @classmethod
    def initfields(cls) -> tuple[Field, ...]:
        return tuple([f for f in fields(cls) if f.init == True])
    
    @classmethod
    @cache
    def initfields_keys(cls) -> list[str]:
        return [i.name for i in cls.initfields()]
    
    @classmethod
    def post_init_descriptors(cls) -> dict[str, BaseDescriptor]:
        return filter_dict(descriptorsmap(cls), lambda x: x.post_init_factory is not MISSING)
    
    @classmethod
    def fieldsmap(cls) -> dict[str, Field]:
        return make_dict_from_iterable(cls.fields(), key_func=lambda x: get_attr_or_item(x, 'public_name'))
    
    @classmethod
    def safe_create(cls, *args, **kwargs) -> Self:
        return cls(*args, **{k: v for k, v in kwargs.items() if k in cls.initfields_keys() if not is_null(v)})
    
    @classmethod
    def fullvars(cls) -> dict[str, Any]:
        return {**ChainMap(*[vars(b) for b in cls.mro()])}
    
    @classmethod
    def display_properties(cls):
        return cls.DISPLAY_PROPERTIES or tuple()
    
    def __post_init__(self):
        for d in self.post_init_descriptors().values():
            if is_null(getattr(self, d.public_name)):
                setattr(self, d.public_name, d.post_init_factory())
    
    @classmethod
    def table(cls):
        return cls.TABLE or cls.clsname()
    
    @classmethod
    def item_name(cls):
        return cls.ITEM_NAME or slug(cls.clsname())
    
    @classmethod
    def singular(cls):
        return cls.SINGULAR or cls.clsname()
    
    @classmethod
    def plural(cls):
        return cls.PLURAL or f'{cls.singular()}s'

    @classmethod
    def clsname(cls):
        return cls.__name__
    
    @classmethod
    def fields(cls) -> tuple[Field, ...]:
        return fields(cls)
    
    # @classmethod
    # def fieldsmap(cls):
    #     return make_dict(cls.fields(), key_func=lambda x: x.name)
    
    @classmethod
    def dataclass_bases(cls) -> tuple:
        return tuple([b for b in cls.mro() if is_dataclass(b)])
    
    @classmethod
    def descriptorsmap(cls) -> dict[str, BaseDescriptor]:
        return descriptorsmap(cls)
    
    @classmethod
    def descriptors(cls) -> tuple[BaseDescriptor]:
        return descriptors(cls)
    
    @classmethod
    def descriptorskeys(cls):
        return tuple([i.public_name for i in cls.descriptors()])
    
    def asjson(self, exclude: list[str] = None):
        return json_parse(exclude_keys_from_dict(asdict(self), exclude or list()))
    
    def asjson_to_db(self):
        return json_parse(filter_dict_by_keys(asdict(self), only=db_descriptorsmap(self).keys()))


context = copy_context()


ModelMap: ChainMap[str, type[BaseModel]] = ChainMap()

def get_models(mm: ModelMap = ModelMap):
    return list((i for i in mm.values()))

def get_models_by_key_name(key_name: str, mm: ModelMap = ModelMap):
    return (i for i in get_models(mm) if key_name in i.descriptorskeys())


setattr(ModelMap, 'get_models', partial(get_models))
setattr(ModelMap, 'facility_key_models', partial(get_models_by_key_name, key_name='facility_key'))
setattr(ModelMap, 'patient_key_models', partial(get_models_by_key_name, key_name='patient_key'))
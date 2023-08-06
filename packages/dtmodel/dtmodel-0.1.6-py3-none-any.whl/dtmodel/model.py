from __future__ import annotations

__all__ = [
        'context_model',
        'Model',
        'compare_descriptors',
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
        'exist_query',
        'descriptors',
        'display_items',
        'display_repr',

]

from starlette.datastructures import QueryParams
from deta.base import FetchResponse
from dtmodel.base import *
from dtmodel.parse import *
from dtmodel.descriptor import *
from dtmodel.functions import *
from dtmodel.endpoint.base import *


def exist_query(self: Model):
    if not self.exist_params():
        raise ValueError(f'{self.clsname()} não definiu EXIST_PARAMS')
    qr = None
    if isinstance(self.exist_params(), str):
        qr = json_parse(query_from_string(self, self.exist_params()))
    elif isinstance(self.exist_params(), list):
        qr = json_parse(
                list(filter(lambda x: is_null(x) is False, [query_from_string(self, i) for i in self.exist_params()])))
    if isinstance(qr, list):
        if len(qr) == 1:
            return qr[0]
    return qr



@dataclass
class Model(BaseModel):
    CTXVAR: ClassVar[ContextVar] = None
    DETA_QUERY: ClassVar[Optional[DetaQuery]] = None
    EXIST_PARAMS: ClassVar[DetaQuery] = None
    DELETABLE: ClassVar[bool] = True
    TABLEDATA: ClassVar[dict[str, dict]] = None
    DATALIST_PATH: ClassVar[str] = '/datalist/{}'
    LIST_PATH: ClassVar[str] = '/list/{}'
    NEW_PATH: ClassVar[str] = '/new/{}'
    DETAIL_PATH: ClassVar[str] = '/detail/{}/{}'
    DELETE_PATH: ClassVar[str] = '/delete/{}/{}'
    UPDATE_PATH: ClassVar[str] = '/update/{}/{}'

    key: str = Validator(default=None, frozen=True, compare=False, label='Chave', hash=False)

    
    @classmethod
    def datalist_path(cls, **kwargs):
        return f'{cls.DATALIST_PATH.format(cls.item_name())}?{QueryParams(kwargs)}'
    
    @classmethod
    def list_path(cls, **kwargs):
        return f'{cls.LIST_PATH.format(cls.item_name())}?{QueryParams(kwargs)}'
    
    @classmethod
    def new_path(cls, **kwargs):
        return f'{cls.NEW_PATH.format(cls.item_name())}?{QueryParams(kwargs)}'
    
    def detail_path(self, **kwargs):
        return f'{self.DETAIL_PATH.format(self.item_name())}?{QueryParams(kwargs)}'
    
    def delete_path(self, **kwargs):
        return f'{self.DELETE_PATH.format(self.item_name())}?{QueryParams(kwargs)}'
    
    async def delete(self):
        if self.DELETABLE:
            return await DetaBase(self.table()).delete(getattr(self, 'key'))
        print(f'{self.clsname()}.FROZEN is True and cannot be deleted')
        return
    
    @classmethod
    def exist_params(cls):
        return cls.EXIST_PARAMS
    
    @classmethod
    async def set_tabledata(cls, query: DetaQuery = None):
        cls.TABLEDATA = {key(i): i for i in await cls.fetch_all(query or cls.DETA_QUERY)}
        
    @classmethod
    async def set_if_none_tabledata(cls, query: DetaQuery = None):
        if not cls.TABLEDATA:
            cls.TABLEDATA = {key(i): i for i in await cls.fetch_all(query or cls.DETA_QUERY)}
            
    @classmethod
    async def update_tabledata(cls, query: DetaQuery = None):
        async with create_task_group() as tks:
            for item in cls.model_dependants():
                if item == cls:
                    tks.start_soon(item.set_if_none_tabledata, query or item.DETA_QUERY)
                else:
                    tks.start_soon(item.set_if_none_tabledata, item.DETA_QUERY)
    
    async def exist_response(self):
        return await DetaBase(self.table()).fetch(exist_query(self))
    
    async def save(self):
        data = self.asjson_to_db()
        new = await DetaBase(self.table()).put(data=data)
        if new:
            await self.set_tabledata()
            return self.safe_create(**new)
        return None
    
    async def save_new(self):
        exist = await self.exist_response()
        if exist.count == 0:
            return await self.save()
        elif exist.count == 1:
            return self.safe_create(**exist.items[0])
        else:
            return None
    
    async def update_instance(self, **kwargs):
        current = self.asjson()
        current.update(exclude_keys_from_dict(kwargs, exclude=['key']))
        key = current.pop('key')
        await DetaBase(self.table()).put(data=current, key=key)
        await self.set_tabledata()
        return self.from_context(key)
    
    @classmethod
    def dependant_descriptors(cls):
        return {d.public_name: d for d in has_dependants_descriptors(cls)}
    
    @classmethod
    def model_dependants(cls, collection: list = None) -> list[type[Model]]:
        return model_dependants(cls, collection or list())
    
    @classmethod
    def from_context(cls, key: str = None) -> Self:
        if key is None:
            return None
        data = cls.get_context().get(key, None)
        if data:
            return cls.safe_create(**data)
        return None
    
    @classmethod
    def from_tabledata(cls, key: str = None) -> Self:
        if key is None:
            return None
        data = cls.TABLEDATA.get(key, None)
        if data:
            return cls.safe_create(**data)
        return None
    
    @classmethod
    async def set_context(cls, data: Optional[dict[str, dict]] = None):
        if not data:
            context.run(cls.CTXVAR.set, make_dict_from_iterable(await cls.fetch_all()))
        else:
            context.run(cls.CTXVAR.set, data)
    
    @classmethod
    def get_context(cls):
        return cls.TABLEDATA or context.get(cls.CTXVAR)
    
    @classmethod
    async def fetch_all(cls, query: DetaQuery = None) -> list[dict[str, Jsonable]]:
        return await DetaBase(cls.table()).fetch_all(query or cls.DETA_QUERY)
    
    @classmethod
    async def fetch(cls, query: DetaQuery = None, last: Optional[str] = None, limit: int = 1000) -> FetchResponse:
        return await DetaBase(cls.table()).fetch(query or cls.DETA_QUERY, last, limit)
    
    @classmethod
    async def update_context(cls):
        async with create_task_group() as tks:
            for item in cls.model_dependants():
                tks.start_soon(item.set_context, item.TABLEDATA)
    
    def __lt__(self, other):
        return normalize_lower(str(self)) < normalize_lower(str(other))
    
    @classmethod
    async def instances_list(cls, query: Optional[dict[str, Any]] = None) -> list[Self]:
        await cls.update_tabledata(query)
        instances = [cls.from_tabledata(i) for i in cls.TABLEDATA.keys()]
        # if query:
        #     print(query)
        #     return [i for i in instances if all([*[getter(i, k) == v for k, v in query.items() if v]])]
        return instances
    
    @classmethod
    async def instances_list_contains(cls, query: Optional[dict[str, str]] = None) -> list[Self]:
        await cls.update_tabledata(query)
        instances = [cls.from_tabledata(i) for i in cls.TABLEDATA.keys()]
        # if query:
        #     print(query)
        #     return [i for i in instances if all([*[normalize_lower(str(getter(i, k))).__contains__(normalize_lower(str(v))) for k, v in query.items() if v]])]
        return instances
    
    @classmethod
    async def sorted_list(cls, query: dict[str, Any] = None) -> list[Self]:
        return sorted(await cls.instances_list(query=query))
    
    @classmethod
    async def sorted_list_contains(cls, query: dict[str, str] = None) -> list[Self]:
        return sorted(await cls.instances_list_contains(query=query))
    
    @classmethod
    async def ordered_list(cls, query: dict[str, Any] = None) -> list[Self]:
        return ordered(await cls.instances_list(query=query))
    
    @classmethod
    async def ordered_lis_containst(cls, query: dict[str, Any] = None) -> list[Self]:
        return ordered(await cls.instances_list_contains(query=query))

    @classmethod
    def key_name(cls):
        return f'{cls.item_name()}_key'
    
    
    # @classmethod
    # async def response_new(cls, request: Request):
    #     patient_key = pk(request)
    #     patient = None
    #     if patient_key:
    #         Patient: Model = ModelMap.get('Patient')
    #         await Patient.update_tabledata()
    #         patient = Patient.from_tabledata(patient_key)
    #         print(patient)
    #     if request.method == 'GET':
    #         return HTMLResponse(TEMPLATES.get_template(f'partial/form/{cls.item_name()}/new.jj').render(
    #                 request=request,
    #                 patient=patient,
    #                 model=cls
    #         ))
    #     elif request.method == 'POST':
    #         data = {**await request.form()}
    #         await cls.update_tabledata()
    #         if patient_key:
    #             data['patient_key'] = patient_key
    #         instance = cls.safe_create(data)
    #         new = await instance.save_new()
    #         if new:
    #             return HTMLResponse(TEMPLATES.get_template('partial/detail/index.jj').render(
    #                     request=request,
    #                     patient=patient,
    #                     model=cls,
    #                     instance=new
    #             ))
    #         return HTMLResponse('erro')
    #
    # @classmethod
    # async def response_detail(cls, request: Request):
    #     patient_key = pk(request)
    #     await cls.update_tabledata()
    #     if patient_key:
    #         Patient: Model = ModelMap.get('Patient')
    #         request.state.patient = Patient.from_tabledata(patient_key)
    #         request.state.instance = cls.from_tabledata(request.path_params.get(cls.key_name()))
    #         return HTMLResponse(TEMPLATES.get_template('partial/detail/index.jj').render(
    #                 request=request,
    #                 patient=request.state.patient,
    #                 instance=request.state.instance,
    #                 model=cls
    #         ))
    #     else:
    #         request.state.instance = cls.from_tabledata(request.path_params.get(cls.key_name()))
    #         return HTMLResponse(TEMPLATES.get_template('partial/detail/index.jj').render(
    #                 request=request,
    #                 instance=request.state.instance,
    #                 model=cls
    #         ))
    #
    #
    # @classmethod
    # async def response_list(cls, request: Request) -> TEMPLATES.TemplateResponse:
    #     patient_key = pk(request)
    #     if patient_key:
    #         Patient: Model = ModelMap.get('Patient')
    #         request.state.patient = Patient.from_tabledata(patient_key)
    #         request.state.instances = await cls.sorted_instances_list({'patient_key': patient_key})
    #         return HTMLResponse(TEMPLATES.get_template('partial/list/index.jj').render(
    #                 request=request,
    #                 patient=request.state.patient,
    #                 instances=request.state.instances,
    #                 model=cls
    #
    #         ))
    #     else:
    #         request.state.instances = await cls.sorted_instances_list()
    #         return HTMLResponse(TEMPLATES.get_template('partial/list/index.jj').render(
    #                 request=request,
    #                 instances=request.state.instances,
    #                 model=cls
    #
    #         ))
        
        

def model_dependants(obj: type[Model], collection: list = None):
    collection = collection or list()
    for item in obj.dependant_descriptors().values():
        models = item.dependants
        for model in models:
            if not model in collection:
                collection = model_dependants(model, collection)
    if not obj in collection:
        collection.append(obj)
    return collection


def context_model(cls: type[Model]):
    @wraps(cls)
    def wrapper():
        cls.CTXVAR = ContextVar(f'{cls.__name__}Var')
        cls.__repr__ = partialmethod(repr_func)
        cls.__eq__ = partialmethod(eq_function)
        ModelMap[cls.__name__] = cls
        ModelMap[cls.item_name()] = cls
        if not cls.exist_params():
            raise ValueError(f'Cadastrar EXIST_PARAMS para a class {cls}')
        return cls
    return wrapper()


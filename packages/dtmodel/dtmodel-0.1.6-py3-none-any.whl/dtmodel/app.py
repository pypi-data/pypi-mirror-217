__all__ = ['App']

import re
from dataclasses import dataclass
from enum import Enum

import uvicorn
from typing import Protocol, Union, Callable, Coroutine, Awaitable
from collections import ChainMap, UserDict
from starlette.applications import Starlette
from starlette.routing import Route, Mount, Router
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.middleware import Middleware
from anyio import create_task_group
from dtmodel.endpoint.middleware import Session
from dtbase import config, DetaBase
from dtmodel.model import Model
from dtmodel.models import *
from dtmodel.functions import *
from dtmodel import ModelMap
from markupsafe import Markup
from dtmodel.endpoint.base import *
    

def model_endpoint_constructor(md: type[Model], endpoint_function: Callable[[type[Model], Request], Coroutine]):
    async def endpoint(request: Request):
        return await endpoint_function(md, request)
    return endpoint


def endpoint_constructor(template: str):
    async def endpoint(request: Request):
        return await render(template, request)
    return endpoint

async def dashboard_home(request: Request):
    await Patient.update_tabledata()
    print(RequestData(request).data)
    return TEMPLATES.TemplateResponse('partial/dashboard/index.jj', {
            'request': request,
            'patient': Patient.from_tabledata(pk(request)),
    })


async def dashboard_model_list(model: Model):
    async def endpoint(request: Request):
        patient_key = pk(request)
        await Patient.update_tabledata()
        return TEMPLATES.TemplateResponse(f'partial/list/index.jj').render(
                request=request,
                patient=Patient.from_tabledata(patient_key),
                instances=await model.sorted_list(dict(patient_key=patient_key)),
                model=model
        )
    return endpoint


async def dashboard_end(request: Request):
    req = RequestData(request)
    model_item = req.url_model_item
    if model_item:
        model = req.model(model_item)
        return await dashboard_list(model, req)
        
    else:
        return await dashboard_home(request)
        


async def dashboard_list(model: type[Model], request: Request):
    async def endpoint(request: Request):
        patient_key = pk(request)
        await Patient.update_tabledata()
        return TEMPLATES.TemplateResponse(f'partial/list/index.jj').render(
                request=request,
                patient=Patient.from_tabledata(patient_key),
                instances=await model.sorted_list(dict(patient_key=patient_key)),
                model=model
        )
    return endpoint


def endpoint_dashboard_delete(model: Model):
    async def endpoint(request: Request):
        await DetaBase(model.table()).delete(request.path_params[model.key_name()])
        await model.update_tabledata()
        patient = Patient.from_tabledata(pk(request))
        return TEMPLATES.TemplateResponse('partial/dashboard/index.jj', {
                'request': request,
                'patient': patient,
                'model': model,
                'instances': await model.sorted_list({'patient_key': pk(request)})
        })
    return endpoint

# def endpoint(model: Model, template: str = 'partial/dashboard/index.jj'):
#     async def endpoint(request: Request):
#         return TEMPLATES.TemplateResponse(template, await endpoint_data(request, model=model))
#     return endpoint

async def endpoint_data(request: Request, model: Model = None):
    data = {'request': request}
    pk = ChainMap(request.path_params, request.query_params).get('patient_key')
    if pk:
        await Patient.update_tabledata()
        data['patient'] = Patient.from_tabledata(pk)
    if not_null(model) and isinstance(model, type) and issubclass(model, Model):
        await model.update_tabledata()
        data['instances'] = await model.sorted_list({**request.query_params})
        data['model'] = model
    return data


    

def make_endpoint(func, model: Model):
    return func(model)
    

async def render_dashboard(request: Request, template: str):
    await Patient.update_tabledata()
    patient = Patient.from_tabledata(pk(request))
    return TEMPLATES.TemplateResponse(template, {
            'request': request,
            'patient': patient
    })

async def patient_search(request: Request):
    search = request.query_params.get('search', None)
    query = {f'{k}?contains': normalize_lower(str(v)) for k,v in request.query_params.items()}
    
    def none():
        return HTMLResponse(Markup('<h3 class="text-center p-4">nada encontrado</h3>'))
    
    if search:
        model = ModelMap.get(request.path_params.get('item_name'))
        await model.update_tabledata()
        instances = await model.sorted_list(query)
        if len(instances) == 0:
            return none()
        return TEMPLATES.TemplateResponse('partial/search/index.jj', {
                'request': request,
                'instances': instances
        })
    return none()

def endpoint(func: Callable, *args, **kwargs):
    async def dynamic_endpoint(request: Request):
        return await func(request, *args, **kwargs)
    return dynamic_endpoint


async def request_data(request: Request):
    query = {**request.query_params}
    data = {'request': request}
    patient_key = request.path_params.get('patient_key')
    if patient_key:
        await Patient.update_tabledata()
        data['patient'] = Patient.from_tabledata(patient_key)
    item = request.path_params.get('item_name')
    if item:
        data['item_name'] = item
        model = ModelMap.get(item)
        await model.update_tabledata()
        data['model'] = model
        item_key = request.path_params.get('item_key')
        if item_key:
            instance = model.from_tabledata(item_key)
            if instance: data['instance'] = instance
        else:
            if patient_key:
                query.update({'patient_key': patient_key})
            data['instances'] = await model.sorted_list(query)
    return data



home_route = Route('/', endpoint_constructor(template='index.jj'), name='home')
static_mount = Mount('/static', app=STATIC, name='static')
wellcome_home = Route('/wellcome', endpoint_constructor(template='partial/session/index.jj'))
# patient_seach = Route('/patient/search', patient_search, name='search')
search_route = Route('/{item_name}/search', patient_search, name='search')

# path params bases routes

class RequestData(UserDict):
    def __init__(self, request: Request):
        self.request = request
        data = dict(request=request)
        data['action'] = self.action
        data['patient_key'] = request.path_params.get('patient_key')
        data['item_name'] = request.path_params.get('item_name')
        data['item_key'] = request.path_params.get('item_key')
        super().__init__(data)
        self.data['model'] = self.model

    async def fetch(self, query = None):
        query = query or dict()
        if self.patient_key:
            query['patient_key'] = self.patient_key
        
        async def fetch_patient():
            if self.patient_key:
                await self.patient_model().update_tabledata()
                self.data['patient'] = self.patient_model().from_tabledata(self.patient_key)

        async def fetch_model():
            if self.model:
                await self.model.update_tabledata()
                if self.item_key:
                    self.data['instance'] = self.model.from_tabledata(self.item_key)
                else:
                    if self.action == 'list':
                        self.data['instances'] = await self.model.sorted_list(query)
        
        async with create_task_group() as tks:
            for item in [fetch_model, fetch_patient]:
                tks.start_soon(item)
                
    @classmethod
    def patient_model(cls) -> Model:
        return ModelMap.get('Patient')
        
        
    @property
    def model(self) -> Model:
        if self.item_name:
            return ModelMap.get(self.item_name)
        return None
    
    @property
    def item_name(self):
        return self.data.get('item_name')
    
    @property
    def action(self):
        return self.data.get('action')
    
    @property
    def patient_key(self):
        return self.data.get('patient_key')
    
    @property
    def item_key(self):
        return self.data.get('item_key')
    
    @property
    def action(self):
        return re.search(r'(new|datalist|list|delete|detail|form|dashboard)', self.request.url.path).group(0)
    
    class Action(Enum):
        NEW = '/new'
        LIST = '/list'
        DATALIST = '/datalist'
        DETAIL = '/detail'
        FORM = '/form'
        DELETE = '/delete'
    #
    # action: Action = None
    # patient_key: str = None
    # item_name: str = None
    #
    # def __post_init__(self):
    #     self.action = self.request.path_params.get('action')
    #     self.patient_key = self.request.path_params.get('patient_key')
    #     self.item_name = self.request.path_params.get('item_name')
        


def mkendpoint(template: str):
    
    async def model_dispatcher(data: dict):
        req = data['request']
        md = data['model']
        if req.method == 'GET':
            await md.update_tabledata()
            return HTMLResponse(TEMPLATES.get_template(template).render(**data))
        
    async def patient_key_model_dispatcher(data: dict):
        pk = data['patient_key']
        req = data['request']
        md = data['model']
        if req.method == 'GET':
            await md.update_tabledata()
            return HTMLResponse(TEMPLATES.get_template(template).render(**data))
        
            
    async def endpoint(request: Request):
        data = {**ChainMap(request.path_params, request.query_params)}
        data.update(await request_data(request))
        rq = RequestData(request)
        await rq.fetch()
        print(rq)

        if request.method == 'GET':
            if not request.path_params.get('patient_key'):
                return await model_dispatcher(data)
            return HTMLResponse(Markup(TEMPLATES.get_template(template).render(**data)))
        
        elif request.method == 'POST':
            if '/delete' in request.url.path:
                await data['instance'].delete()
                return HTMLResponse('<span class="text-muted">objeto excluído com sucesso</span>', 303)
            elif '/new' in request.url.path:
                form_data = {**await request.form()}
                if form_data.get('key'):
                    form_data.pop('key')
                obj = data['model'].safe_create(**form_data)
                new = await obj.save_new()
                if new:
                    data['instance'] = new
                    if request.path_params.get('patient_key'):
                        tp = TEMPLATES.get_template(f'dashboard/patient/action/model/index.jj').render(**data)
                    else:
                        tp = TEMPLATES.get_template(f'dashboard/action/model/index.jj').render(**data)
                else:
                    return HTMLResponse('os dados não foram processados')
                return HTMLResponse(Markup(tp), 303)
        
    return endpoint

model_datalist_route = Route('/datalist/{item_name}', mkendpoint('dashboard/action/model/index.jj'))
model_list_route = Route('/list/{item_name}', mkendpoint('dashboard/action/model/index.jj'))
model_new_route = Route('/new/{item_name}', mkendpoint('dashboard/action/model/index.jj'), methods=['GET', 'POST'])
model_form_route = Route('/form/{item_name}', mkendpoint('dashboard/action/model/index.jj'))
model_detail_route = Route('/detail/{item_name}/{item_key}', mkendpoint('dashboard/action/model/index.jj'))

mount_dashboard = Mount('/dashboard', name='dashboard', routes=[
        Route('/', mkendpoint('dashboard/index.jj'), name='home'),
        Mount('/{patient_key}',name='patient', routes=[
                Route('/', mkendpoint('dashboard/patient/index.jj'), name='detail'),
                Mount('/{action}', routes=[
                        Route('/', mkendpoint('dashboard/patient/action/index.jj'), name='action'),
                        Mount('/{item_name}', routes=[
                                Route('/', mkendpoint('dashboard/patient/action/model/index.jj'), name='item_name', methods=['GET', 'POST']),
                                Route('/{item_key}', mkendpoint('dashboard/patient/action/model/instance/index.jj'), methods=['GET', 'POST'])
                              ]),
                ])
        ]),

])

app_routes = [
        static_mount,
        search_route,
        model_datalist_route,
        model_list_route,
        model_new_route,
        model_form_route,
        mount_dashboard,
        model_detail_route,

]



def create_model_mount(name: str, constructor: Callable[[type[Model], Callable], Callable], partial_endpoint: Callable[[type[Model], Request], Coroutine] , mds: list[type[Model]]) -> Mount:
    return Mount(
            f'/{name}',
            name=name,
            routes=[
                    Route(f'/{model.item_name()}', constructor(model, partial_endpoint), name=model.item_name()) for model in mds
            ]
    )

# dashboard_model_list_mount = Mount(
#         '/list',
#         name='list',
#         routes=[
#                 Route(f'/{model.item_name()}', endpoint(model, 'partial/list/index.jj'), name=model.item_name())
#                 for model in ModelMap.patient_key_models()
#         ]
# )

# model_list_mount = create_model_mount('list', model_endpoint_constructor, response, [*ModelMap.values()])

# model_delte_mount = Mount(
#         '/delete',
#         name='delete',
#         routes=[
#                 Route(f'/{model.item_name()}/{{{model.key_name()}}}', endpoint_dashboard_delete(model=model), name=model.item_name(), methods=['GET', 'POST'])
#                 for model in ModelMap.patient_key_models()
#         ]
# )

async def endpoint_new(request: Request):
    # await Patient.update_tabledata()
    model: Model = ModelMap.get(request.path_params.get('item_name'))
    # patient = Patient.from_tabledata(pk(request))
    # return HTMLResponse(TEMPLATES.get_template(f'partial/form/{item_name}/new.jj').render(
    #         patient=patient,
    #         request=request,
    #         model=model
    # ))
    return await model.response_new(request)


async def patient_display(request: Request):
    await Patient.update_tabledata()
    patient = Patient.from_tabledata(pk(request))
    return HTMLResponse(TEMPLATES.get_template('partial/patient/index.jj').render(
            request=request,
            instance=patient,
            patient=patient,
            model=Patient
    ))

# dashboard_mount = Mount(
#         '/dashboard/{patient_key}',
#         name='dashboard',
#         routes=[
#                 Route('/', dashboard_home, name='home'),
#                 Route('/new/{item_name}', endpoint_new, name='new', methods=['GET', 'POST']),
#                 model_delte_mount,
#                 Mount('/list', name='list', routes=[
#                         Route(f'/{m.item_name()}', m.response_list, name=m.item_name()) for m in list(ModelMap.patient_key_models())
#                 ]),
#                 *[Route(f'/{m.item_name()}/{{{m.key_name()}}}', m.response_detail, name=m.item_name()) for m in list(ModelMap.patient_key_models())]
#         ]
# )

# class RequestData(UserDict):
#     def __init__(self, request: Request):
#         self.request = request
#         self.match = re.match(r'/(P:<action>new|list|detail|delete|update)/(P:<model_item>{})'.format('|'.join([i.item_name() for i in ModelMap.values()])), self.request.url.path)
#         if self.match:
#             self.groupdict = self.match.groupdict()
#         else:
#             self.groupdict = dict()
#         super().__init__({
#                 'request': request,
#                 'patient_key': request.path_params.get('patient_key', request.query_params.get('patient_key')),
#                 **self.groupdict
#         })
#
#     @property
#     def patient_key(self):
#         return self.data.get('patient_key')
#
#
#     @property
#     def url_action(self):
#         return self.data.get('actiion')
#
#     @property
#     def url_model_item(self):
#         return self.data.get('model_item')
#
#     @property
#     def method(self):
#         return self.request.method
#
#     @property
#     def path_params(self):
#         return self.request.path_params
#
#     @property
#     def query_params(self):
#         return self.request.query_params
#
#     @property
#     def full_params(self):
#         return {**ChainMap(self.request.path_params, self.request.query_params)}
#
#     @property
#     def dashboard(self):
#         return True if 'dashboard' in self.request.url.path else False
#
#
#     @staticmethod
#     def model(name: str) -> type[Model]:
#         return ModelMap.get(name)
#
#
#


def route_constructor(template: str = 'index.jj'):
    async def route_endpoint(request: Request):
        req = RequestData(request)
        print(req.data)
        if req.patient_key:
            await req.model('Patient').update_tabledata()
        if req.url_model_item:
            await req.model(req.url_model_item).update_tabledata()
        return TEMPLATES.TemplateResponse(template, req.data)
    return route_endpoint
    



patient_detail = Route('/patient/{patient_key}', patient_display, name='patient')

class App(Starlette):
    def __init__(self,
                 debug=False,
                 routes: list[Union[Route, Mount, Router]]=None,
                 middleware: list[Middleware] = None
                 ):
        self.user_routes = routes or list()
        self.user_middleware = middleware or list()
        super().__init__(
                debug=debug,
                routes= [*app_routes, *self.user_routes],
                # routes=[home_route, static_mount, patient_seach, patient_detail, self.dashboard_mount, *self.user_routes],
                # routes=[home_route, static_mount, wellcome_home, patient_seach, patient_detail, dashboard_mount, *self.user_routes],
                middleware=[Session, *self.user_middleware]
        )
        
        
    def dashboard_mount(self):
        return Mount(f'/dashboard', name='dashboard', routes=[
                Route('/', dashboard_end, name='home'),
                Route('/search', patient_search, name='search'),
                Mount('/{patient_key}', name='patient', routes=[
                        Route('/', dashboard_home, name='detail'),
                        Route('/{action}/{model}', dashboard_end, name='action'),
                        Route('/{action}/{model}/{item_key}', dashboard_end, name='item')
                
                ]),
        
        ])
        
        
    def run(self, host: str = None or str(), port: int = config.get('PORT', cast=int, default=777), **kwargs):
        uvicorn.run('main:app', host=host, port=port, reload=True, **kwargs)
        
        
    
        

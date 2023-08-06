__all__ = [
        'TEMPLATES',
        'STATIC',
        'pk',
        'origin',
        'api_key',
        'headers',
        'EndpointData',
        'deta_api_key',
        'detabase_project_key',
        'deta_space_app_micro_name',
        'deta_space_app_micro_type',
        'deta_space_app',
        'deta_project_key',
        'deta_space_app_hostname',
        'deta_space_app_version',
        'PresetEnv'
]

import os
from collections import namedtuple
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.routing import Route, Router, Mount
from dtmodel.base import *
from dtmodel.parse.json_encoder import json_parse
from dtmodel.functions import *
from markupsafe import Markup

def deta_space_app_hostname() -> str:
    return config.get("DETA_SPACE_APP_HOSTNAME", cast=str)

def deta_space_app() -> bool:
    return config.get("DETA_SPACE_APP", cast=bool)

def deta_space_app_version():
    return config.get('DETA_SPACE_APP_VERSION')

def port():
    return config.get('PORT')

def deta_space_app_micro_name():
    return config.get('DETA_SPACE_APP_MICRO_NAME')


def deta_space_app_micro_type():
    return config.get('DETA_SPACE_APP_MICRO_TYPE')

def deta_api_key():
    return config.get('DETA_API_KEY')

def detabase_project_key():
    return config.get('DETABASE_PROJECT_KEY')


def deta_project_key():
    return config.get('DETA_PROJECT_KEY')

def origin():
    return f"https://{config.get('DETA_SPACE_APP_HOSTNAME')}"

def api_key():
    return config.get("DETA_API_KEY")


def headers():
    return {"x-api-key": api_key()}


try:
    TEMPLATES: Jinja2Templates = Jinja2Templates(directory=os.path.join(os.getcwd(), 'templates'))
    TEMPLATES.env.globals['config'] = config
    TEMPLATES.env.globals['ModelMap'] = ModelMap
    TEMPLATES.env.globals['Markup'] = Markup
    TEMPLATES.env.globals['pkmodels'] = lambda : list([*set([i for i in ModelMap.values() if hasattr(i, 'patient_key')])])
    TEMPLATES.env.globals['fkmodels'] = lambda : list([*set([i for i in ModelMap.values() if hasattr(i, 'facility_key')])])
    TEMPLATES.env.globals['get_model'] = lambda name: ModelMap.get(name)
    TEMPLATES.env.globals['form_descriptors'] = lambda model: tuple([i for i in descriptors(model) if i.form_field])
    TEMPLATES.env.globals['local_date_format'] = local_date_format
    TEMPLATES.env.globals['public_descriptors'] = public_descriptors
    TEMPLATES.env.globals['random_string'] = random_string
    TEMPLATES.env.globals['local_now'] = local_now
    TEMPLATES.env.globals['local_today'] = local_today
except:
    TEMPLATES: Jinja2Templates = None

try:
    STATIC: StaticFiles = StaticFiles(directory=os.path.join(os.getcwd(), 'static'))
    Static: Mount = Mount('/static', app=STATIC, name='static')
except:
    STATIC: StaticFiles = None
    Static: Mount = None
    
    
class EndpointData(UserDict):
    MICRO_NAMES: ClassVar[list[str]] = None
    def __init__(self, request: Request):
        data = dict(request=request)
        super().__init__(data)
        
    @property
    def patient_key(self):
        return self.request.path_params.get('patient_key', self.request.query_params.get('patient_key'))
    
    @property
    def item_name(self):
        return self.request.path_params.get('item_name')
    
    @property
    def model(self):
        if self.item_name:
            return ModelMap[self.item_name]
        return None
    
    @property
    def jsonable_data(self):
        return {
                'instance': self.data.get('instance', None),
                'instances': self.data.get('instances', list()),
                'patient': self.data.get('patient', None)
        }
    
    @property
    def item_key(self):
        return self.request.path_params.get('item_key')
    
    @property
    def action(self):
        return self.request.path_params.get('action')
    
    @classmethod
    def get_model(cls, name: str):
        return ModelMap.get(name)
    
    def query(self):
        q = {**self.request.query_params}
        if self.patient_key:
            q['patient_key'] = self.patient_key
        return q
        
    @property
    def request(self) -> Request:
        return self.data.get('request')
    
    async def process_patient(self):
        if self.patient_key:
            try:
                self.data['patient'] = self.get_model('Patient').from_tabledata(self.patient_key)
            except:
                await ModelMap['Patient'].update_tabledata()
                self.data['patient'] = ModelMap['Patient'].from_tabledata(self.patient_key)
        
    async def process_model(self):
        if self.action:
            if self.action in ('detail', 'delete'):
                self.data['instance'] = self.model.from_tabledata(self.item_key)
            elif self.action in ('list', 'datalist'):
                self.data['instances'] = await self.model.sorted_list(self.query())
                
    async def process(self):
        await self.process_patient()
        await self.process_model()
        if self.request.method == 'POST':
            self.data['form_data'] = await self.request.form()
            result = dict()
            for k, v in self.data['form_data'].items():
                if isinstance(v, (list, tuple)):
                    result[k] = [*v]
                else:
                    result[k] = v
            self.data['form_result'] = result
        return self

    
def endpoint(template: str = None):
    async def dispatcher(request: Request):
        if request.method == 'GET':
            ctx = await EndpointData(request).process()
            if template:
                return HTMLResponse(TEMPLATES.get_template(template).render(**ctx))
            return JSONResponse(json_parse(ctx.jsonable_data))
        elif request.method == 'POST':
            ctx = await EndpointData(request).process()
            instance = ctx.model.safe_create(**ctx.get('form_result'))
            new = await instance.save_new()
            if new:
                ctx['created'] = new
                return HTMLResponse(TEMPLATES.get_template(f'api/detail/{ctx.item_name}/{new.key}').render(**ctx))
            return HTMLResponse(TEMPLATES.get_template(template).render(**ctx))
    return dispatcher
    

async def update_model_tabledata(model: 'Model'):
    await model.set_tabledata()
    

# class RouteEnum(Enum):
#     HOME = Route('/', endpoint('index.jj'), name='home')
#     STATIC = Mount('/static', app=STATIC, name='static')
#     PATIENT_KEY = Route('/{patient_key}', endpoint('dash/index.jj'), name='patient_key')
#     ACTION = Route('/{action}/{item_name}', endpoint('api/index.jj'), name='action', methods=['GET', 'POST'])
#     JSON = Route('/{action}/{item_name}', endpoint('json/index.jj'), name='json', methods=['GET', 'POST'])
#
# class MicroConfig(namedtuple('Micro', 'path routes primary engine', defaults=[False, 'python3.9']), Enum):
#     FRONT = '/', [RouteEnum.HOME.value, RouteEnum.STATIC.value], True
#     DASHBOARD = '/dash', [RouteEnum.PATIENT_KEY.value]
#     API = '/api', [RouteEnum.ACTION.value]
#     JSON = '/json', [RouteEnum.JSON.value]
#
# def get_mount(micro_config: MicroConfig):
#     return Mount(micro_config.value.path, routes=micro_config.value.routes, name=micro_config.name.lower())

    
# class MicroMount(Enum):
#     FRONT = get_mount(MicroConfig.FRONT)
#     DASHBOARD = get_mount(MicroConfig.DASHBOARD)
#     API = get_mount(MicroConfig.API)
#     JSON = get_mount(MicroConfig.JSON)
    
def pk(request: Request) -> str:
    return request.path_params.get('patient_key', request.query_params.get('patient_key', None))
    
    
# async def render(template: str, request: Request, data: dict = None):
#     data = data or dict()
#     data.update({'request': request})
#     return TEMPLATES.TemplateResponse(template, data)


# class TemplateMap(Enum):
#     INDEX = TEMPLATES.get_template('index.jj')
#     DASHBOARD= TEMPLATES.get_template('dashboard/index.jj')
#     DASHBOARD_NEW = TEMPLATES.get_template('dashboard/new.jj')
#     DASHBOARD_LIST = TEMPLATES.get_template('dashboard/list.jj')
#     DASHBOARD_DETAIL = TEMPLATES.get_template('dashboard/detail.jj')
#     DASHBOARD_DATALIST = TEMPLATES.get_template('dashboard/datalist.jj')

    
# class TemplatePath(namedtuple('TemplatePath', 'path description', defaults=['']),Enum):
#     INDEX = 'index.jj', 'base for all templates'
#     INDEX_MACROS = 'macros.jj.jj', 'index template with macro functions'
#     PARTIAL = 'partial/', 'partial directory'
#     PARTIAL_INDEX = 'partial/index.jj', 'partial index template'
#     PARTIAL_MACROS = 'partial/macros.jj.jj', 'partial directory macros.jj'
#     SESSION = 'partial/session/', 'session directory for auth, login, logout, register'
#     SESSION_INDEX = 'partial/session/index.jj', 'session index template'
#     SESSION_MACROS = 'partial/session/macros.jj.jj', 'session directory macros.jj'
#     FORM = 'partial/form/', 'form directory'
#     FORM_INDEX = 'partial/form/index.jj', 'form index template'
#     FORM_NEW_PRESCRIPTION = 'partial/form/new/prescription.jj'
#     FORM_NEW_EVENT = 'partial/form/new/event.jj'
#     FORM_NEW_INVOICE = 'partial/form/new/invoice.jj'
#     FORM_MACROS = 'partial/form/macros.jj.jj', 'form directory macros.jj'
#     LIST = 'partial/list/', 'list directory'
#     LIST_INDEX = 'partial/list/index.jj', 'list index template'
#     LIST_MACROS = 'partial/list/macros.jj.jj', 'list directory macros.jj'
#     DETAIL = 'partial/detail/', 'detail directory'
#     DETAIL_INDEX = 'partial/detail/index.jj', 'detail index templates'
#     DETAIL_MACROS = 'partial/detail/macros.jj.jj', 'detail directory macros.jj'
#     DASHBOARD = 'partial/dashboard/', 'dashboard directory'
#     DASHBOARD_INDEX = 'partial/dashboard/index.jj', 'dashboard index templates'
#     DASHBOARD_MACROS = 'partial/dashboard/macros.jj.jj', 'dashboard template for macros.jj'
#
# class TemplateEnv(namedtuple('TemplateEnv', 'name description'), Enum):
#     MODELS_MAP = 'ModelsMap', 'todos as classes adicionadas pelo decorador @context_model'
#     NAV_MODELS = 'NavModels', 'classes destinadas à compor a nav'
#     PATIENT_MODELS = 'PatientModels', 'classes que possuem como atributo "patient_key"'
#     FACILITY_MODELS = 'FacilityModels', 'classes que possuem como atributo "facility_key"'
#
#
# class TemplatePaths(namedtuple('TemplatePaths', 'path description', defaults=['']),Enum):
#     INDEX = 'index.jj', 'base for all templates'
#     INDEX_MACROS = 'macros.jj.jj', 'index template with macro functions'
#     PARTIAL = 'partial/', 'partial directory'
#     PARTIAL_INDEX = 'partial/index.jj', 'partial index template'
#     PARTIAL_MACROS = 'partial/macros.jj.jj', 'partial directory macros.jj'
#     SESSION = 'partial/session/', 'session directory for auth, login, logout, register'
#     SESSION_INDEX = 'partial/session/index.jj', 'session index template'
#     SESSION_MACROS = 'partial/session/macros.jj.jj', 'session directory macros.jj'
#     FORM = 'partial/form/', 'form directory'
#     FORM_INDEX = 'partial/form/index.jj', 'form index template'
#     FORM_NEW_PRESCRIPTION = 'partial/form/new/prescription.jj'
#     FORM_NEW_EVENT = 'partial/form/new/event.jj'
#     FORM_NEW_INVOICE = 'partial/form/new/invoice.jj'
#     FORM_MACROS = 'partial/form/macros.jj.jj', 'form directory macros.jj'
#     LIST = 'partial/list/', 'list directory'
#     LIST_INDEX = 'partial/list/index.jj', 'list index template'
#     LIST_MACROS = 'partial/list/macros.jj.jj', 'list directory macros.jj'
#     DETAIL = 'partial/detail/', 'detail directory'
#     DETAIL_INDEX = 'partial/detail/index.jj', 'detail index templates'
#     DETAIL_MACROS = 'partial/detail/macros.jj.jj', 'detail directory macros.jj'
#     DASHBOARD = 'partial/dashboard/', 'dashboard directory'
#     DASHBOARD_INDEX = 'partial/dashboard/index.jj', 'dashboard index templates'
#     DASHBOARD_MACROS = 'partial/dashboard/macros.jj.jj', 'dashboard template for macros.jj'
#

class PresetEnv(namedtuple('PresetEnv', 'description default', defaults=['']), Enum):
    SESSION_SECRET = 'secret key to be used in session middleware'
    DETABASE_PROJECT_KEY = 'data_key to access your deta Base data'
    USER_KEY = 'user_key to idenfity the creator of objects if not logging in after deta space login'
    USER_PASSWORD = 'password to check the user_key in database'
    FACILITY_NAME = 'name of the facility'
    FACILITY_ADDRESS = 'address of the facility'
    FACILITY_CITY = 'city and state of the facility'
    FACILITY_PHONE = 'phone number of the facility'
    FACILITY_EMAIL = 'email of the facility'
    DETA_AUTH_KEY = 'auth_key to access other deta space app if necessary'
    
    
    @classmethod
    def keys(cls):
        text = ''
        for m in cls.__members__.values():
            text += "\t\t- name: {}\n\t\t  description: {}\n".format(m.name, m.value.description)
        return text
    
    @classmethod
    def spacefile(cls):
        return """
v: 0
icon: src/front/static/img/logo.png
micros:
  - name: front
    src: ./src/front
    engine: python3.9
    primary: true
    path: /
    presets:
      api_keys: true
      env:
{}""".format(cls.keys())
    
    
#
# class BaseEndpoint(HTTPEndpoint):
#     def __init__(self, *args, template: str = 'index.jj', **kwargs):
#         self.template = template
#         super().__init__(*args, **kwargs)
#
#     async def render(self, request: Request, **kwargs):
#         return TEMPLATES.get_template(self.template).render(**self.request_url_data(request))
#
#     @staticmethod
#     def patient_key(request: Request):
#         return request.path_params.get('patient_key', request.query_params.get('patient_key'))
#
#     @staticmethod
#     def find_action(request: Request):
#         match = re.match(r'(P<action>patient|list|delete|detail|update|new)', request.url.path)
#         if match:
#             return match.group('action')
#         return None
#
#     @staticmethod
#     def find_model(request: Request):
#         match = re.match(r'(P<model>{})'.format("|".join([i.item_name() for i in ModelMap.values()])), request.url.path)
#         if match:
#             return match.group('model')
#         return None
#
#     @staticmethod
#     def model(name: str) -> 'Model':
#         return ModelMap.get(name)
#
#     @staticmethod
#     def request_url_data(request: Request):
#         data = {'request': request}
#         data.update({**request.query_params})
#         data.update({**request.path_params})
#         return data
#
#     @classmethod
#     async def process_patient_key(cls, request: Request):
#         pk = request.path_params.get('patient_key', request.query_params.get('patient_key'))
#         if pk:
#             Patient = cls.model('Patient')
#             await Patient.update_tabledata()
#             return Patient.from_tabledata(pk)
#         return None
#
#     def route(self):
#         return
#
#     async def get(self, request: Request):
#         data = self.request_url_data(request)
#         patient = await self.process_patient_key(request)
#         if patient: data['patient'] = patient
#
#         if model:
#             md = self.model(model)
#             await md.update_tabledata()
#             mdkey = request.path_params.get(md.key_name())
#             if mdkey:
#                 data['instance'] = model.from_tabledata(mdkey)
#             else:
#                 if pk:
#                     data['instances'] = await model.sorted_list({'patient_key': pk})
#                 else:
#                     data['instances'] = await model.sorted_list()
#         if action:
#             return HTMLResponse(TEMPLATES.get_template(f'{action}/index.jj').render(
#                     **data
#             ))
#         return HTMLResponse(TEMPLATES.get_template(f'index.jj').render(
#                 **data
#         ))

# class MicroRouter(Router):
#     def __init__(self,
#                  micro: MicroMount,
#                  ):
#         self.micro = micro
#         super().__init__(
#                 routes=[self.micro.value],
#         )
#
#     def run(self, host: str = None or str(), port: int = config.get('PORT', cast=int, default=777), **kwargs):
#         uvicorn.run('main:app', host=host, reload=True, **kwargs)
#

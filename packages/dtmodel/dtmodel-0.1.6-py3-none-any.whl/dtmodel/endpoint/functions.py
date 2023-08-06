#
#
# from starlette.endpoints import HTTPEndpoint
# from starlette.requests import Request
# from dtmodel.base import *
# from dtmodel.endpoint.base import *
# from dtmodel.model import *
#
#
# class Endpoint(HTTPEndpoint):
#     URL_PATTERN = re.compile(r'(P:<action>/list|/new|/update|/delete|/dashboard|/search)?(P:<model>{})?'.format('|'.join(set([i.item_name() for i in ModelMap.values()]))))
#     def __init__(self, model: type[Model] = None, *args, **kwargs):
#         self.model = model
#         super().__init__(*args, **kwargs)
#
#     @property
#     def items_names(self):
#         return '|'.join(set([i.item_name() for i in ModelMap.values()]))
#
#     @staticmethod
#     def pk(request: Request):
#         return request.path_params.get('patient_key', request.query_params.get('patient_key'))
#
#     def get_action(self, request: Request):
#         return re.search(r'(P:<action>/list|/new|/update|/delete|/dashboard|/search)', request.url.path).groupdict().get('action')
#
#
#
#     async def get(self, request: Request):
#         url_matchs = self.URL_PATTERN.match(request.url.path).groupdict()
#         action, model = url_matchs.get('action'), url_matchs.get('model')
#
#
#
#
#     def template_path(self, request: Request):
#         subpath = re.search(r'(P:<action>/list|/new|/update|/delete|/dashboard|/search)')
#         model = re.search(r'(P:<model>{})'.format(self.items_names))
#
#         dt = list()
#         pk = self.pk(request)
#         if pk:
#             dt.append(f'/dashboard/{pk}')
#         if model:
#             dt.append(f'/{subpath.__getitem__("action")}/{model.__getitem__("model")}')
#         return ''.join(dt)
#
#
# class GetEndpoint(HTTPEndpoint):
#     def __init__(self, model: type[Model] = None, *args, **kwargs):
#         self.model = model
#         super().__init__(*args, **kwargs)
#
#
#
#
#

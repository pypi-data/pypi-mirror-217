# __all__ = [
#         'Render', 'response'
# ]
#
# from enum import Enum
# from collections import UserString
# from anyio import create_task_group
# from dtmodel.endpoint.base import TEMPLATES
# from dtmodel.base import *
# from dtmodel.model import *
# from dtmodel.models import *
# from dtmodel.functions import *
#
# from markupsafe import Markup
#
#
# async def update_tabledata(models: list[Type[Model]]):
#     async with create_task_group() as tks:
#         for model in models:
#             if model:
#                 tks.start_soon(model.set_tabledata)
#
# def packmodel(request: Request):
#     math = re.search(r'(P<item_name>{})'.join(f'|'.join([m.item_name() for m in ModelMap.values()])), request.url.path)
#     if math:
#         item_name = math.group(0)
#         print(item_name)
#         request.state.model = first([i for i in ModelMap.values() if i.item_name() == item_name])
#     else:
#         request.state.model = None
#     return request
#
# def packpath(request: Request):
#     match = re.search(r'(P<path>new|delete|datalist|list|update)', request.url.path)
#     if match:
#         path = match.group(0)
#     else:
#         path = 'detail'
#     print(path)
#     request.state.path = path
#     return request
#
#
# def packpatient(request: Request):
#     request.state.pk = request.path_params.get('patient_key', request.query_params.get('patient_key'))
#     return request
#
#
# def pack(request: Request):
#     return packpath(packmodel(packpatient(request)))
#
# async def compose(request: Request):
#     request = pack(request)
#     await update_tabledata([Patient, request.state.model])
#     if request.state.model:
#         if request.state.pk:
#             request.state.data = {
#                     request.state.model.clsname(): await request.state.model.sorted_list(
#                             {'patient_key': request.state.pk})
#             }
#     return request
#
#
#
#
# async def response(request: Request):
#     request = await compose(request)
#     print(request.state.pk, request.state.model, request.state.path)
#     if all([request.state.pk, request.state.model, request.state.path]):
#         return TEMPLATES.get_template(f'partial/{request.state.path}/index.jj').render(
#                 request=request,
#                 patient=Patient.from_tabledata(request.state.pk),
#                 instances= await request.state.model.sorted_list({'patient_key': request.state.pk})
#         )
#     elif all([request.state.pk, request.state.path]):
#         return TEMPLATES.get_template(f'partial/dashboard/index.jj').render(request=request, patient=Patient.from_tabledata(request.state.pk))
#     elif all([request.state.pk]):
#         return TEMPLATES.get_template(f'partial/dashboard/index.jj').render(request=request)
#
#
#
# class Render:
#     def __init__(self, request: Request, template: str = 'index.jj', **kwargs):
#         self.request = request
#         self._template = template
#         self._kwargs = kwargs
#         self.data = dict()
#
#     def __html__(self):
#         return TEMPLATES.get_template('partial/detail/index.jj').render()
#
#     @property
#     def model(self):
#         return None if not hasattr(self, 'model') else getattr(self, 'model')
#
#     @staticmethod
#     def patient_key(request: Request):
#         return request.path_params.get('patient_key', request.query_params.get('patient_key'))
#
#     def template(self):
#         return self._template.format(**self._kwargs.values())
#
#     async def list(self, request: Request, model: type[Model], **kwargs):
#         pk = self.patient_key(request)
#         if pk:
#             if model != Patient:
#                 return TEMPLATES.get_template(f'/dashboard/{pk}/list/{model.item_name()}').render(
#                         request=request,
#                         model=model,
#                         patient=Patient.from_tabledata(pk),
#                         instances= await model.sorted_list({'patient_key': pk}),
#                         **kwargs
#                 )
#         else:
#             return TEMPLATES.get_template(f'/dashboard/{pk}/list/{model.item_name()}').render(
#                     request=request,
#                     model=model,
#                     patient=Patient.from_tabledata(pk),
#                     instances=await model.sorted_list(),
#                     **kwargs
#             )
#
#

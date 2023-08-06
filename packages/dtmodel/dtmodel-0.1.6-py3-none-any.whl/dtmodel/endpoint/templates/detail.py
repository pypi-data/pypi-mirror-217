# __all__ = [
#         'Detail'
# ]
#
# from enum import Enum
# from collections import UserString
# from dtmodel.endpoint.base import TEMPLATES
# from dtmodel.base import *
# from dtmodel.model import *
# from markupsafe import Markup
#
#
#
# class Detail:
#     def __init__(self, instance: Model):
#         self.instance = instance
#
#     def __html__(self):
#         return TEMPLATES.get_template('partial/detail/index.jj').render(instance=self.instance)

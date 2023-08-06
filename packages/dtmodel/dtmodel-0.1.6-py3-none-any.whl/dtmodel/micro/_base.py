
__all__ = [
        'action',
        'micro',
        'item_name',
        'item_key',
        'PathParts',
        'path_search',
        'item_names'
]


from dtmodel.base import *


ACTION_NAMES = ('new', 'list', 'datalist', 'detail', 'delete')
MICRO_NAMES = ('html', 'json', 'dash')


def path_search(names: tuple[str], string: str):
    search = re.search(r'(?<=/)({})'.format("|".join(names)), string)
    if search:
        return search.group(0)
    return None



action = partial(path_search, ACTION_NAMES)
micro = partial(path_search, MICRO_NAMES)

def item_names() -> tuple[str]:
    return tuple([i.item_name() for i in set(ModelMap.values())])
    

def item_name(string: str):
    return path_search(item_names(), string)

def item_key(string: str):
    name = item_name(string)
    if name:
        result = re.search(r'(?<=/{}/)([._\w]+)'.format(name), string)
        if result:
            return result.group(0)
    return None


class PathParts(UserString):
    def __init__(self, value: str):
        self.micro = micro(value)
        if self.micro == 'dash':
            self.action = None
            self.item_name = item_name(value)
            self.item_key = item_key(value)
        else:
            self.action = action(value)
            self.item_name = item_name(value)
            if self.action in ('detail', 'delete'):
                self.item_key = item_key(value)
            else:
                self.item_key = None
        super().__init__(value)
    
    @property
    def parts(self):
        return self.micro, self.action, self.item_name, self.item_key
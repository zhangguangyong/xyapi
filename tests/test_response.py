import json

from xyapi.response import Ok, CustomJsonEncoder

if __name__ == '__main__':
    print(json.dumps(Ok({'name': 'x'}), cls=CustomJsonEncoder))
    pass

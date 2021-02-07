import json
from responses._base import Response as BaseResponse

class Response(BaseResponse):
    def __init__(self, application, request):
        super().__init__(application, request)

    def json(self):
        about = {}
        about['module_id'] = 'print_server'
        about['module_name'] = 'Форматирование и печать отчетов'
        about['version'] = f'{self.application.version}'
        return json.dumps(about, ensure_ascii=False)
    
    def __call__(self):
        return f'Форматирование и печать отчетов, версия {self.application.version}'

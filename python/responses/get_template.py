import os, sys, json
from flask import make_response
from domino.core import log

from responses._base import Response as BaseResponse
from tables.postgres.print_template import PrintTemplate
 
class Response(BaseResponse):
    def __init__(self, application, request):
        super().__init__(application, request)
    
    def __call__(self):
        template_id = self.get('template_id')
        if not template_id:
            return f'Не задан template_id', 500
        print_template = self.postgres.query(PrintTemplate).get(template_id)
        if not print_template:
            return f'Не найден {template_id}', 500
        response  = make_response(print_template.template_frx)
        response.headers['Content-Type'] = 'text/plain'
        #response.headers['Content-Description'] = 'File Transfer'
        response.headers['Content-Disposition'] = f'inline'
        #response.headers['Content-Disposition'] = f'attachment; filename=label.{label.id}.dataset.xml'
        response.headers['Content-Length'] = len(print_template.template_frx)
        #response.headers['Cache-Control'] = 'no-store'
        return response




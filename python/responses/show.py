import os, sys, json
from responses._base import Response as BaseResponse
from flask import make_response
from tables.postgres.print_queue_item import PrintQueueItem

class Response(BaseResponse):
    def __init__(self, application, request):
        super().__init__(application, request)
    
    def dataset(self):
        id = self.get('id')
        print_queue_item = self.postgres.query(PrintQueueItem).get(id)
        response  = make_response(print_queue_item.dataset)
        response.headers['Content-Type'] = 'application/xml'
        #response.headers['Content-Description'] = 'File Transfer'
        response.headers['Content-Disposition'] = f'inline'
        #response.headers['Content-Disposition'] = f'attachment; filename=label.{label.id}.dataset.xml'
        response.headers['Content-Length'] = len(print_queue_item.dataset)
        #response.headers['Cache-Control'] = 'no-store'
        return response



import flask, json
from domino.core import log

class Response:
    def __init__(self, application, request):
        self.application = application
        self.request = request
        self.account_id = self.request.args.get('account_id')

    def get(self, name):
        return self.request.args.get(name)
    
    def __call__(self):
        return ''

    def make_response(self, fn=None):
        log.debug(f'{fn}')

        if fn:
            f = getattr(self, fn)
            if f is None:
                return f'{fn} ?', 500
            return f()
        else:
            return self.__call__()

    def success(self, msg = None):
        r = {'status':'success'}
        if msg:
            r['message'] = msg
        return json.dumps(r, ensure_ascii=False)


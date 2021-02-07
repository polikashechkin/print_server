from domino.core import log
from responses._base import Response as BaseResponse
from tables.postgres.server import Server
from tables.postgres.printer import Printer

class Response (BaseResponse):

    def __init__(self, application, request):
        super().__init__(application, request)

    def __call__(self):
        server_id = self.get('server_id')
        if not server_id:
            return f'Не задан сервер приложений', 500
        printer_name = self.get('name')
        if not printer_name:
            return f'Не задано имя принтера', 500
        driver_name = self.get('driver_name')
        server = self.postgres.query(Server).get(server_id)
        if not server:
            return f'Не найден сервер "{server_id}"'
        printer = self.postgres.query(Printer).filter(Printer.name == printer_name, Printer.server_id == server_id).one_or_none()
        if printer:
            if printer.description is None:
                printer.description = {}
            printer.description['driver_name'] = driver_name
            #log.debug('update description')
        else:
            printer = Printer(server_id = server_id, state = 0, name = printer_name, description = {'driver_name':driver_name})
            self.postgres.add(printer)
        return self.success()

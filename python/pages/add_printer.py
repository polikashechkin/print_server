from domino.core import log
from pages._base import Page as BasePage
from pages._base import Title, Toolbar, Input, InputText, Button, Select
from tables.postgres.printer import Printer
from tables.postgres.server import Server
#from domino.postgres import Postgres
#from dicts.dept_dict import DeptDict

class Page(BasePage):
    def __init__(self, application, request):
        super().__init__(application, request)

    #def add_param(self, description, param_name):
    #    value = self.get(param_name)
    #    if value:
    #        description[param_name] = value
    #    return value

    def add_printer(self):
        printer = Printer()

        printer.server_id = self.get('server_id')
        #printer.dept_code = self.get('dept_code')
        #if not printer.dept_code:
        #    self.error('Код подразделения должен быть задан')
        #    return
        #-------------------------------------    
        printer.name = self.get('name')
        if not printer.name:
            self.error('Имя должно быть задано')
            return
        #printer.print_server_name = self.get('print_server_name')
        #width = self.get('width')
        #if width:
        #    printer.width = int(width)
        #else:
        #    self.error('Ширина должна быть задана')
        #height = self.get('height')
        #if height:
        #    printer.height = int(height)
        #-------------------------------------    
        #printer.name = self.get('name')
        #-------------------------------------    
        self.postgres.add(printer)
        self.message('Добавлено')

    def __call__(self):
        Title(self, 'Принтер')

        #dept_params = Toolbar(self, 'dept_params')
        #depts = DeptDict(self.account_id)
        #select = Select(dept_params.item(mr=1), label='Подразделение', name='dept_code')
        #for code, name in depts.items():
        #    select.option(code, f'{code}, {name}')

        #Input(dept_params.item(mr=1), label='Код подразделения', name='dept_code')
        #Input(dept_params.item(mr=1), label='Адрес подразделения', name='dept_address').width(30)

        base_params = Toolbar(self, 'base_params')
        select = Select(base_params.item(mr=1), label='Сервер', name='server_id')
        for server in self.postgres.query(Server):
            select.option(server.id, server.name)

        Input(base_params.item(mr=1), label='Имя принтера на сервере', name='name')
        #params = Toolbar(self, 'params').mt(1)
        ##Input(params.item(mr=1), label='Ширина', name='width')
        #Input(params.item(mr=1), label='Высота', name='height')

        toolbar = Toolbar(self, 'toolbar').mt(1)
        Button(toolbar, 'Добавить').onclick('.add_printer', forms=[base_params])

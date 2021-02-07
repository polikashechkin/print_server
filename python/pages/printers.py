import json
from domino.core import log
from pages._base import Page as BasePage
from pages._base import Title, Toolbar, Input, InputText, Button, Table, IconButton, Select, Row
from tables.postgres.printer import Printer
from tables.postgres.server import Server
#from tables.dept import Dept
from sqlalchemy import or_, and_

class Page(BasePage):
    def __init__(self, application, request):
        super().__init__(application, request)
    
    def delete(self):
        printer_id = self.get('printer_id')
        #printer = self.postgres.query(Printer).get(printer_id)
        
        #sql = 'delete from "printer" where "id"=%s'
        #self.pg_cursor.execute(sql, [ID])
        self.Row('table', printer_id)
        self.message(f'Удален принтрер {printer_id}')

    def change_disabled(self):
        printer_id = self.get('printer_id')
        printer = self.postgres.query(Printer).get(printer_id)
        server = self.postgres.query(Server).get(printer.server_id)
        printer.disabled = not printer.disabled
        row = Row(self, 'table', printer.id)
        self.print_row(row, printer, server)

    def print_complex_cell(self, cell, name, params):
        if params is not None and len(params) > 0:
            cell.html(f'''{name}<p style="font-size:small;color:gray; line-height: 1em">{', '.join(params)}</p>''')
        else:
            cell.text(name)

    def print_row(self, row, printer, server):
        cell = row.cell(width=2)
        if printer.disabled:
            IconButton(cell, 'check', style='color:lightgray')\
                .onclick('.change_disabled', {'printer_id':printer.id})
        else:
            IconButton(cell, 'check', style='color:green')\
                .onclick('.change_disabled', {'printer_id':printer.id})
        row.cell(width=1).text(printer.id)
        self.print_complex_cell(row.cell(), server.name, [server.id])
        params = []
        if printer.description is not None:
            params.append(json.dumps(printer.description, ensure_ascii=False))
        self.print_complex_cell(row.cell(), printer.name, params)
        #row.cell().text(printer.width)
        #row.cell().text(printer.height)
        cell = row.cell(width=6, align='right')
        #IconButton(cell, 'edit', style='color:lightgray').onclick('pages/printer', {'printer_id' : printer.id})
        IconButton(cell, 'close', style='color:red').onclick('.delete', {'printer_id' : printer.id})

    def print_table(self):
        table = Table(self, 'table').mt(0.5)
        table.column()
        table.column().text('#')
        table.column().text('Сервер')
        table.column().text('Принтер')
        #table.column().text('Подразделение')
        #table.column().text('Ширина')
        #table.column().text('Высота')
        table.column()
        query = self.postgres.query(Printer, Server).filter(Printer.server_id == Server.id)
        server_id = self.get('server_id')
        if server_id:
            query = query.filter(Server.id == server_id)
        
        mode = self.get('mode')
        if mode != 'all':
            query = query.filter(or_(Printer.disabled == False, Printer.disabled == None))

        for printer, server in query.order_by(Printer.id.desc()):
            row = table.row(printer.id)
            self.print_row(row, printer, server)
   
    def print_toolbar(self):
        toolbar = Toolbar(self, 'toolbar')
        select = Select(toolbar.item(), label='Режим просмотра', name='mode')\
            .onclick('.print_table', forms=[toolbar])
        select.option('','ТОЛЬКО АКТИВНЫЕ УСТРОЙСТВА')
        select.option('all','ВСЕ УСТРОЙСТВА')

        select = Select(toolbar.item(ml=1), label='Сервер', name='server_id')\
            .onclick('.print_table', forms=[toolbar])
        select.option('','')
        for server in self.postgres.query(Server):
            select.option(server.id, server.name)
        Button(toolbar.item(ml='auto'), 'Добавить вручную').onclick('pages/add_printer')

    def __call__(self):
        Title(self, 'Устройства печати')
        self.print_toolbar()
        self.print_table()

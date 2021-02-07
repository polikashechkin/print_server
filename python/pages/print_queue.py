import requests, os, html
from domino.core import log, DOMINO_ROOT
from pages._base import Page as BasePage
from pages._base import Title, Toolbar, Input, InputText, Button, Text, Select, Table, Row, IconButton
from tables.postgres.server import Server
from tables.postgres.print_queue_item import PrintQueueItem

class Page(BasePage):
    def __init__(self, application, request):
        super().__init__(application, request)

    def delete(self):
        id = self.get('id')
        self.postgres.query(PrintQueueItem).filter(PrintQueueItem.id == id).delete()
        Row(self, 'table', id)
 
    def print_complex_cell(self, cell, name, params):
        if len(params) > 0:
            comment = html.escape(', '.join(params))
            comment = comment[:1000] + '...'
            cell.html(f'''{name}<p style="font-size:small;color:gray; line-height: 1em">{comment}</p>''')
        else:
            cell.text(name)
    
    def print_row(self, row, item, server):
        cell = row.cell(width=2).text(item.id)
        self.print_complex_cell(row.cell(), f'{item.printer_name}, {server.name}', [item.dataset])
        cell = row.cell(width=6, align='right')
        IconButton(cell, 'file_download', style='color:lightgray').onclick('show.dataset', {'id':item.id, 'account_id':self.account_id}, target='NEW_WINDOW')
        IconButton(cell, 'close', style='color:red').onclick('.delete', {'id':item.id})

    #def folder(self, server_id):
    #    return os.path.join(DOMINO_ROOT, 'accounts', self.account_id, 'requests', server_id, 'print_server')

    def print_table(self, server_id = None): 
        if not server_id:
            server_id = self.get('server_id')

        table = Table(self, 'table').mt(1)
        query = self.postgres.query(PrintQueueItem, Server).join(Server, Server.id == PrintQueueItem.server_id)
        if server_id:
            query = query.filter(PrintQueueItem.server_id == server_id)
        for item, server in query.order_by(PrintQueueItem.ctime.desc()):
            row = table.row(item.id)
            self.print_row(row, item, server)

    def __call__(self):
        Title(self, 'Очередь на печать')
        toolbar = Toolbar(self, 'toolbar')
        select = Select(toolbar.item(), name='server_id')\
            .onchange('.print_table', forms=[toolbar])
        select.option('', '')
        server_id = None
        for server in self.postgres.query(Server):
            if server_id is None:
                server_id = server.id
            select.option(server.id, f'{server.name}')

        self.print_table(None)

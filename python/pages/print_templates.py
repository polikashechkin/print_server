import json
from domino.core import log
from pages._base import Page as BasePage
from pages._base import Title, Toolbar, Input, InputText, Button, Table, Row, IconButton
from tables.postgres.print_template import PrintTemplate

class Page(BasePage):
    def __init__(self, application, request):
        super().__init__(application, request)

    def print_complex_cell(self, cell, name, params):
        if len(params) > 0:
            cell.html(f'''{name}<p style="font-size:small;color:gray; line-height: 1em">{', '.join(params)}</p>''')
        else:
            cell.text(name)

    def print_table(self):
        table = Table(self, 'table').mt(0.5).css('table-borderless')
        #table.column()
        #table.column().text('ID')
        #table.column().text('Наименование')
        #table.column().text('Размеры')
        #table.column().text('Последнее обновление')
        #table.column()
        for print_template in self.postgres.query(PrintTemplate):
            row = table.row(print_template.id)
            row.cell().text(print_template.id)
            #------------------------------------
            params = []
            columns = print_template.structure.get('columns')
            if columns is not None:
                for column_name, column_info in columns.items():
                    column_type = column_info.get('type')
                    params.append(f'{column_name}')
            self.print_complex_cell(row.cell(), f'{print_template.name}', params)
            cell = row.cell(width=6, align='right')
            row.cell(align='right').text(print_template.mtime)
            #------------------------------------
            cell = row.cell(align='right')
            Button(cell, 'шаблон')\
                .onclick('get_template', {'account_id':self.account_id, 'template_id':print_template.id}, target='NEW_WINDOW')
            Button(cell, 'набор')\
                .onclick('get_template_dataset', {'account_id':self.account_id, 'template_id':print_template.id}, target='NEW_WINDOW')
            #------------------------------------
            #------------------------------------
            #cell = row.cell(width=15, align='right' )
            #Button(cell, 'Обновить').onclick('.upgrade', {'id' : template.id, 'code':template.code})
            #Button(cell, 'Удалить').onclick('.delete', {'id' : template.id})


    def __call__(self):
        Title(self, 'Шаблоны отчетов')
        self.print_table()

import json, datetime
from domino.core import log
from pages.base_page import Page as BasePage
from pages.base_page import Title, Toolbar, Input, InputText, Button, Select
from tables.postgres.printer import Printer

class Page(BasePage):
    def __init__(self, application, request):
        super().__init__(application, request)
        self.printer_id = self.attribute('printer_id')

    def get_int(self, name):
        value = self.get(name)
        if value:
            return int(value)
        else:
            return None

    def change_printer_params(self):
        printer = self.postgres.query(Printer).get(self.printer_id)
        #printer.modify_time = datetime.datetime.now()
        printer.width = self.get_int('width')
        printer.height = self.get_int('height')
        if not printer.width:
            self.error(f'Ширина должна быть задана')
            return
        self.message(f'Изменено')

    def __call__(self):
        printer = self.postgres.query(Printer).get(self.printer_id)
        Title(self, f'{printer.name}')

        params = Toolbar(self, 'params').mt(1)
        Input(params.item(mr=1), label='Ширина (мм)', name='width', value=printer.width)
        Input(params.item(mr=1), label='Высота (мм)', name='height', value=printer.height)

        toolbar = Toolbar(self, 'toolbar').mt(1)
        Button(toolbar, 'Изменить').onclick('.change_printer_params', forms=[params])

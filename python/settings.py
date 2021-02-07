import os, sys, json, time
import xml.etree.cElementTree as ET
import requests

MODULE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#from sqlalchemy.ext.declarative import declarative_base
#PostgresBase = declarative_base()
MODULE_ID = 'print_server'

from domino.core import log, DOMINO_ROOT, IS_WINDOWS, IS_LINUX
from components.console import Console

if IS_WINDOWS:
    import win32print
    from win32print import PRINTER_ENUM_CONNECTIONS, PRINTER_ENUM_NAME

class Settings:
    def __init__(self):
        c = Console(MODULE_ID)
        self.account_id = c.get('account_id')
        self.server_id = c.get('server_id')
        self.parent_server_url = c.get('parent_server_url')
        self.parent_accounts_folder = c.get('parent_accounts_folder')
        #self.requests_folder = os.path.join(self.parent_accounts_folder, self.account_id, 'requests', 'print_server', self.server_id)
        self.timeout = float(c.get('timeout', 1))
        self.count = int(c.get('count', 0))
        self.PrintFastReport_exe = os.path.join(MODULE_ROOT, 'bin', 'PrintFastReport.exe')

def request_about(server, account_id):
    url = f'https://{server}/print_server/active/python/about'
    r = requests.get(url)
    #print(r.status_code, r.url, r.text)
    if r.status_code != 200:
        print(f'{r.status_code} : {url}')
        return False
    #print('Версия ', r.json()['version'])
    return True

def GET(url, module_id, request, params):
    url = f'https://{url}/{module_id}/active/python/{request}'
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print(f'{r.status_code} : {r.url}')
        print(r.text)
        return None
    return r.text

def get_printers():
    printers = []
    #print('УСТАНОВЛЕННЫЕ ПРИНТЕРА')
    for printer in win32print.EnumPrinters(PRINTER_ENUM_CONNECTIONS | PRINTER_ENUM_NAME,  None,2):
        printer_name = printer.get('pPrinterName')
        driver_name = printer.get('pDriverName')
        if printer_name.lower() in [
            'fax', 'onenote', 'Microsoft XPS Document Writer'.lower(), 'Microsoft Print to PDF'.lower()]:
            continue
        printers.append({'printer_name':printer_name, 'driver_name':driver_name})
    #for printer in printers:
    #    print(f'{printer}')
    return printers

if __name__ == "__main__":
    c = Console(MODULE_ID)

    #print('Настройка сервера печати'.upper())

    dsms_server_info_json = os.path.join(DOMINO_ROOT, 'dsms', 'serverinfo.json')
    if os.path.isfile(dsms_server_info_json):
        with open(dsms_server_info_json) as f:
            dsms_server_info = json.load(f)
        c.set('server_id', dsms_server_info.get('server_id'))
        c.set('server_description', dsms_server_info.get('description'))
        account_id = c.get('account_id')
        if not account_id :
            c.set('account_id', dsms_server_info.get('account'))
    
    parent_server_url = c.input('parent_server_url', 'Адрес основного сервера')
    #parent_accounts_folder = c.input('parent_accounts_folder','Папка учетных записей на основном сервере')

    account_id = c.input('account_id', 'Идентификатор учетной записи')
    if not request_about(parent_server_url, account_id):
        print(f'Сервер "{parent_server_url}" НЕДОСТУПЕН'.upper())
        sys.exit(1)

    #account_folder = os.path.join(parent_accounts_folder, account_id)
    #if not os.path.isdir(account_folder):
    #    print(account_folder)
    #    print(f'Неправильно задана папка учетных записей "{parent_accounts_folder}" или учетная запись "{account_id}"'.upprer())
    #    sys.exit(1)

    server_id = c.input('server_id','Идентификатор сервера')
    #c.set('server_id', server_id)
    server_description = c.input('server_description','Описание данного сервера')

    #print ('РЕГИСТРАЦИЯ СЕРВЕРА')
    if not GET(parent_server_url, 'users_and_depts', 'reg_server', {'account_id':account_id, 'id':server_id, 'name': server_description}):
        print ('ОШИБКА РЕГИСТРАЦИИ СЕРВЕРА')
        sys.exit(1)

    if IS_WINDOWS:
        printers = get_printers()
        #print ('РЕГИСТАЦИЯ НАЙДЕННЫХ ПРИНТЕРОВ')
        for printer in printers:
            printer_name = printer['printer_name']
            driver_name = printer['driver_name']
            params = {
                'account_id' : account_id,
                'server_id' : server_id,
                'name' : printer_name,
                'driver_name' : driver_name
            }
            if not GET(parent_server_url, 'print_server', 'reg_printer', params):
                print(f'Ошибка регистрации принтера {printer_name} ({driver_name})')
                sys.exit(1)

    #c.input('timeout','Частота обращения к серверу (с)')
    input('Нажмите любую клавишу для продолжения ...')
    #c.input('count', 'Количество запросов (0-без ограничений)')


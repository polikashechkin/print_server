import os, sys, json, time, select
import xml.etree.cElementTree as ET
import requests
import psycopg2
import psycopg2.extensions

from domino.core import log, DOMINO_ROOT
from settings import Settings

class PrintJob:

    class TemplateFile:
        def __init__(self, account_id, template_id, version):
            self.account_id = account_id
            self.template_id = template_id
            self.version = version
            self.file_path = os.path.join(DOMINO_ROOT, 'accounts', self.account_id, 'data', 'print_server', 'templates', f'{template_id}', 'template.frx')

        def __str__(self):
            return self.file_path

        def __repr__(self):
            return f'<TemplateFile(account_id={self.account_id}, template_id={self.template_id}, version={self.version}) file_path={self.file_path})>'

        def load_file(self, parent_server_url, log):
            log(f'Обновление шаблона "{self.template_id}", версия "{self.version}"')
            url = f'https://{parent_server_url}/print_server/active/python/get_template'
            params = {'account_id':self.account_id, 'template_id':self.template_id}
            r = requests.get(url, params = params)
            #r.encoding = 'utf-8'
            if r.status_code == 200:
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                #log(f'Запись шаблона в файл "{self.file_path}" ')
                with open(self.file_path, 'wb') as f:
                    f.write(r.content)
            else:
                log(f'{r.status_code} : {r.url}')
                raise Exception(log(f'Ошибка получения шаблона'.upper()))

    def __init__(self):
        settings = Settings()

        self.PRINT_FAST_REPORT_EXE = settings.PrintFastReport_exe
        self.parent_server_url  = settings.parent_server_url # Адрес центрального сервера
        self.account_id  = settings.account_id
        self.server_id = settings.server_id
        self.timeout = 1
        self.template_files = {}
        self.home_folder = os.path.join(DOMINO_ROOT, 'accounts', self.account_id, 'data', 'print_server')
        self.current_dataset_xml = os.path.join(self.home_folder, 'current_dataset.xml')
        os.makedirs(self.home_folder, exist_ok=True)
        self.pid_file = os.path.join(self.home_folder, 'pid')

    def log(self, msg):
        print(msg)

    def get_template_file_path(self, template_id, version):
        template_file = self.template_files.get(template_id)
        if not template_file or template_file.version != version:
            template_file = PrintJob.TemplateFile(self.account_id, template_id, version)
            template_file.load_file(self.parent_server_url, self.log)
            self.template_files[template_id] = template_file
        return template_file.file_path
    
    def print_one_label(self, printer_name, template_id, version, dataset):
        with open(self.current_dataset_xml, 'w') as f:
            f.write(dataset)
        template_file_path = self.get_template_file_path(template_id, version)
        #----------------------------------------------------
        #self.log(f'{datafile_xml_path} : Шаблон {template_id} принтер {printer_name}')
        cmd = F'{self.PRINT_FAST_REPORT_EXE} TEMPLATE="{template_file_path}" DATAFILE="{self.current_dataset_xml}" PRINTERNAME="{printer_name}"'
        error = 0
        try:
            self.log(cmd)
            error = os.system(cmd)
            if error:
                self.log(f'Ошибка запуска "{self.PRINT_FAST_REPORT_EXE}"')
        except BaseException as ex:
            self.log(f'Ошибка запуска "{self.PRINT_FAST_REPORT_EXE}" : {ex}')

    def check_for_break(self):
        with open(self.pid_file) as f:
            pid = f.read()
        return pid != self.pid

    def dowork(self):
        self.pid = f'{os.getpid()}'
        with open(self.pid_file, 'w') as f:
            f.write(self.pid)
        print(f'Процесс "{self.pid}" запущен.')

        SELECT = f'''
            select "id", "printer_name", "template_id", "version", "dataset" 
            from "print_queue_item"
            where "server_id" = '{self.server_id}'
            '''
        DELETE = 'delete from "print_queue_item" where "id" = %s'
        self.connection = psycopg2.connect(host=self.parent_server_url, dbname=f'd{self.account_id}', user=f'u{self.account_id}', password='ljvbyj')
        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with self.connection:
            self.cursor = self.connection.cursor()
            LISTEN = f"LISTEN print_queue_item_{self.server_id};"
            self.cursor.execute(LISTEN)
            self.log(LISTEN)

            count = 0
            while True:
                if self.check_for_break():
                    self.log(f'Процесс "{self.pid}" остановлен')
                    break
                if select.select([self.connection],[],[],self.timeout) == ([],[],[]):
                    count += 1
                    #self.log(count)
                else:
                    self.connection.poll()
                    while self.connection.notifies:
                        notify = self.connection.notifies.pop(0)
                        #self.log(f'Got NOTIFY: {notify.pid}, {notify.channel}, {notify.payload}')
                    self.cursor.execute(SELECT) 
                    for id, printer_name, template_id, version, dataset in self.cursor.fetchall():
                        self.print_one_label(printer_name, template_id, version, dataset)
                        self.cursor.execute(DELETE, [id])
                        #self.connection.commit()
                        #os.remove(datafile_xml_path)
                    #self.do_one_step()
                #time.sleep(self.timeout)
                #count += 1
                #if count % 100 == 0:
                #self.log(count)

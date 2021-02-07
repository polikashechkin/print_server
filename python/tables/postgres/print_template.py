import json, datetime, arrow, re, requests, os
import xml.etree.cElementTree as ET

from domino.core import log, DOMINO_ROOT
from sqlalchemy import Column, BigInteger, Integer, String, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from domino.postgres import Postgres

def on_activate(account_id, on_activate_log):
    Postgres.Table(PrintTemplateTable).migrate(account_id, on_activate_log)

class PrintTemplate(Postgres.Base):
   
    __tablename__ = 'print_template3'

    id              = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True) 
    guid            = Column(String) # Идентификатор шаблона, если шаблон для учетной записи, то своддный идентификатор
    mtime           = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    name            = Column(String)
    description     = Column(JSONB)
    dataset_xml     = Column(String) # Набор даных, определяющих структуру отчетв (dataset.xml)
    template_frx    = Column(String) # Шаблон отчета в формате FarstReport3 (template.fr3)
    structure       = Column(JSONB) # Рписание колонок в dataset.xml d виде  {columns_name : {'type': 'тип'}} 

    def __repr__(self):
         return f"<PrintTemplate(id={self.id}, guid={self.guid}, name={self.name})>" 

    def update_from_repo(self):
        self.mtime = datetime.datetime.now()
        if not self.guid:
            error = f'Невозможно обновить шаблон {self}'
            log.error(error)
            raise Exception(error)
        account_id = os.path.dirname(self.guid)
        label_name = os.path.basename(self.guid)
        if account_id:
            folder = f'https://rs.domino.ru/public/templates/accounts/{account_id}/{label_name}'
        else:
            folder = f'https://rs.domino.ru/public/templates/common/{label_name}'
        # ----------------------------------------------
        r = requests.get(f'{folder}/dataset.xml')
        if r.status_code != 200:
            raise Exception(f'{r.url} : {r.status_code}')
        log.debug(f'{r.text}')
        r.encoding='UTF-8'
        self.dataset_xml = r.text
        log.debug(f'{self.dataset_xml}')
        # ----------------------------------------------
        r = requests.get(f'{folder}/template.fr3')
        if r.status_code != 200:
            raise Exception(f'{r.url} : {r.status_code}')
        r.encoding='UTF-8'
        self.template_frx = r.text
        # ----------------------------------------------
        xml = ET.fromstring(self.dataset_xml)
        xinfo = xml.find('info')
        self.name = xinfo.attrib['name']
        # ----------------------------------------------
        xstructure = xml.find('structure')
        xdataset = xstructure.find('dataset')
        dataset_name = xdataset.attrib['name']
        columns = {}
        for xcolumn in xdataset.findall('column'):
            column_name = xcolumn.attrib['name']
            column_type = xcolumn.attrib['type']
            columns[column_name] = {'type' : column_type}
        self.structure = {'dataset_name' : dataset_name, 'columns' : columns}

PrintTemplateTable = PrintTemplate.__table__
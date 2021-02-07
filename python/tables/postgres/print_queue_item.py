import json, datetime
from domino.core import log
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index, BigInteger, String, JSON, DateTime
from domino.postgres import Postgres

def on_activate(account_id, msg_log):
    table =  Postgres.Table(PrintQueueItemTable)
    table.migrate(account_id, msg_log)

class PrintQueueItem(Postgres.Base):
   
    __tablename__ = 'print_queue_item'

    id          = Column(BigInteger, primary_key=True,nullable=False, autoincrement=True)
    ctime       = Column(DateTime)
    server_id   = Column(String, nullable=False)
    printer_name   = Column(String)
    template_id = Column(BigInteger)
    version     = Column(String)
    dataset     = Column(String)

    Index('', server_id, ctime)

    def __repr__(self):
         return f"<PrintQueue(id={self.id}, server_id={self.server_id})>" 
    
PrintQueueItemTable = PrintQueueItem.__table__
       

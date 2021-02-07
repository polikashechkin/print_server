import json, datetime
from domino.core import log
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index, BigInteger, String, JSON, DateTime, Boolean
from domino.postgres import Postgres

def on_activate(account_id, msg_log):
    table =  Postgres.Table(PrinterTable)
    table.migrate(account_id, msg_log)

class Printer(Postgres.Base):
   
    __tablename__ = 'printer'

    id          = Column(BigInteger, primary_key=True,nullable=False, autoincrement=True)
    server_id   = Column(String, nullable=False)
    name        = Column(String, nullable=False)
    disabled    = Column(Boolean)

    #state       = Column(Integer)
    
    #dept_code   = Column(String)
    #code        = Column(String)
    #modify_time = Column(DateTime)
    #class_name  = Column(String)
    #type_name   = Column(String)
    #name        = Column(String)
    description = Column(JSON)
    info        = Column(JSON)
    #width = Column(Integer)
    #height = Column(Integer)
    Index('', server_id, name, unique = True)

    def __repr__(self):
         return f"<Printer id={self.id}, server_id={self.server_id}, name={self.name}'>" 
    
PrinterTable = Printer.__table__
       

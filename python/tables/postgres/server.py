from sqlalchemy import Column, Integer, String, JSON, DateTime
from domino.core import log
from domino.postgres import Postgres

def on_activate(account_id, msg_log = None):
    table = Postgres.Table(ServerTable)
    table.migrate(account_id, msg_log)

class Server(Postgres.Base):

    __tablename__ = 'server'

    id      = Column(String, primary_key=True, nullable=False)
    name    = Column(String)
    info    = Column(JSON)

    def __repr__(self):
         return f"<Server(id={self.id})>" 

ServerTable = Server.__table__

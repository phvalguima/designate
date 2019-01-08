"""Add RBAC Service table"""


from oslo_log import log as logging
from sqlalchemy import String, DateTime, Enum, Text
from sqlalchemy.schema import Table, Column, MetaData

from designate import utils
from designate.sqlalchemy.types import UUID

LOG = logging.getLogger()

meta = MetaData()

SERVICE_STATES = [
    "UP", "DOWN", "WARNING"
]


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    rbac = Table('rbac', metadata,
                 Column('id', UUID(), default=utils.generate_uuid, primary_key=True),
                 
                 Column('created_at', DateTime, default=lambda: timeutils.utcnow()),
                 Column('updated_at', DateTime, onupdate=lambda: timeutils.utcnow()),
                 
                 Column('project_id', UUID(), nullable=False, unique=False),
                 Column('object_id', UUID(), nullable=False, unique=False),
                 Column('target_tenant', UUID(), nullable=False, unique=False),
                 Column('rbac_action', String(255), nullable=False, unique=False),
                 
                 mysql_engine='InnoDB',
                 mysql_charset='utf8'
    )
    
    rbac.create(checkfirst=True)

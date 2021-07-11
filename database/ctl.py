# 3rd party
import databases
import sqlalchemy
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import Column

DB_URL = "sqlite:///./db.db"
database = databases.Database(DB_URL)

__metadata = sqlalchemy.MetaData()
targets = sqlalchemy.Table(
    "targets",
    __metadata,
    sqlalchemy.Column("mac", sqlalchemy.String(length=17), primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=99)),
    sqlalchemy.Column("description", sqlalchemy.String(length=200)),
    sqlalchemy.Column("ip", sqlalchemy.String(length=15)),
    sqlalchemy.Column("broadcast", sqlalchemy.String(length=15)),
)
__engine = sqlalchemy.create_engine(DB_URL, connect_args={"check_same_thread": False})
__metadata.create_all(__engine)

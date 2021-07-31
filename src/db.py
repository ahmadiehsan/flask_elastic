from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from src.config import get_config

engine = create_engine(
    get_config().DATABASE['URI'],
    convert_unicode=True,
    connect_args={'check_same_thread': False}
)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
SQLAlchemyBase = declarative_base()
SQLAlchemyBase.query = db_session.query_property()

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

USER_ID = "root"
USER_PW = "123456789"

pymysql.install_as_MySQLdb()
engine = create_engine('mysql://{}:{}@localhost/iopet?charset=utf8'.format(USER_ID, USER_PW), convert_unicode=True)
sess = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = sess.query_property()

def init_db():
    import iopet_models
    Base.metadata.create_all(engine)


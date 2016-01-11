from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext import declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up the i18n message factory for our package
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('emc.kb')

ORMBase = declarative.declarative_base()

# some_engine = create_engine('mysql://komdba:k0mdba$@192.168.0.7:3306/komdb?charset=utf8', pool_recycle=3600)
# Session = sessionmaker(bind=some_engine)
# kb_session = Session()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext import declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Set up the i18n message factory for our package
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('emc.kb')

DoFollow = "emc.kb:Do follow"
DoVote = "emc.kb:Do vote"

ORMBase = declarative.declarative_base()

some_engine = create_engine('mysql://kbdba:K0mdba$!9@127.0.0.1:3306/parameters?charset=utf8', pool_recycle=3600)
Session = sessionmaker(bind=some_engine)
kb_session = Session()
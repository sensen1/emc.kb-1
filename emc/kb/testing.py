import os
import tempfile

#import sqlalchemy

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

from zope.component import provideUtility

#from z3c.saconfig.utility import EngineFactory
#from z3c.saconfig.utility import GloballyScopedSession

class Topic(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import emc.memberArea
        import emc.kb
        import emc.theme
        xmlconfig.file('configure.zcml', emc.kb, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.theme, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.memberArea, context=configurationContext)        
#        xmlconfig.file('configure.zcml', eisoo.policy, context=configurationContext)
        # Create database in a temporary file
#        fileno, self.dbFileName = tempfile.mkstemp(suffix='.db')
#        dbURI = 'sqlite:///%s' % self.dbFileName
#        dbEngine = sqlalchemy.create_engine(dbURI)
#        eisoo.forum.ORMBase.metadata.create_all(dbEngine)
#        
#        # Register z3c.saconfig utilities for testing
#        engine = EngineFactory(dbURI, echo=False, convert_unicode=False)
#        provideUtility(engine, name=u"ftesting")
#        
#        session = GloballyScopedSession(engine=u"ftesting", twophase=False)
#        provideUtility(session)
    
    def tearDownZope(self, app):
        pass
        # Clean up the database
#        os.unlink(self.dbFileName)
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'emc.theme:default')        
        applyProfile(portal, 'emc.kb:default')
        applyProfile(portal, 'emc.memberArea:default')
#        applyProfile(portal, 'eisoo.policy:default')

FIXTURE = Topic()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="Topic:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="Topic:Functional")

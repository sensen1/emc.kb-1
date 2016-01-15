import unittest

from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from emc.kb.questionfolder import Iquestionfolder
from emc.kb.questionfolder import questionfolder
class TestContent(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def test_questionfolder(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.questionfolder', 'questionfolder')
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question1',
                             title=u"soft kitty",
                             date=u"date"
                             )
        portal['questionfolder'].invokeFactory('emc.kb.question', 'question2',
                             title=u"monst kitty",
                             date=u"date"
                             )
        numv = portal['questionfolder']
        self.assertEqual(portal['questionfolder'].QuestionNum(),2)
        

        
        

class TestRendering(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING      
        
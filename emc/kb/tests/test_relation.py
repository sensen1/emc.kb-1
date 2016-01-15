import unittest
from plone.app.testing import TEST_USER_ID
from plone.testing.z2 import Browser
from plone.app.testing import setRoles
from emc.kb.testing import INTEGRATION_TESTING
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope import component
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic

from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope import event


class TestRenderer(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
   
    def test_count(self):       
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))        
        portal.invokeFactory('emc.kb.topicfolder', 'tf')
        portal.invokeFactory('emc.kb.questionfolder','qf')
        portal['qf'].invokeFactory('emc.kb.question', 'q1',title='question1')
        intids = getUtility(IIntIds)     
 

        q1=portal['qf']['q1']
        portal['tf'].invokeFactory('emc.kb.topic', 'tc1',title="topc1_tile",
                                   relatedquestion=[RelationValue(intids.getId(q1))],
                                   
                                   ) 
        portal['tf'].invokeFactory('emc.kb.topic', 'tc2',
                                   relatedquestion=[RelationValue(intids.getId(q1))
                                                    ],
                                   
                                   )                 
        t1=portal['tf']['tc1']
        portal['qf'].invokeFactory('emc.kb.question', 'q2',title='question2',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))],
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q3',title='question3',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))],
                                   )        

        catalog = component.getUtility(ICatalog)
        
        qlist = sorted(catalog.findRelations({'to_id': intids.getId(t1)}))
        tlist = sorted(catalog.findRelations({'to_id': intids.getId(q1)}))
       
        self.assertEqual(2, len(qlist))
        self.assertEqual(2, len(tlist))
        q2=portal['qf']['q2']
        t1.relatedquestion=[RelationValue(intids.getId(q1)),RelationValue(intids.getId(q2))]
        event.notify(ObjectModifiedEvent(t1))
        import pdb
        pdb.set_trace() 
        tlist2 = sorted(catalog.findRelations({'to_id': intids.getId(q2)}))         
        self.assertEqual(1, len(tlist2))
        

        
        import transaction
        transaction.commit()
        app = self.layer['app']        
        browser = Browser(app)
        browser.handleErrors = False        
        browser.open(t1.absolute_url())
        
        open('/tmp/test.html','w').write(browser.contents)
        
        self.assertTrue("topc1_tile" in browser.contents)
        self.assertTrue("question100" in browser.contents)
        

                
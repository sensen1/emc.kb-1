import unittest
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.layout.navigation.interfaces import INavigationRoot

from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope.component import getUtility, getMultiAdapter
from zope import component
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope import event

from z3c.relationfield import RelationValue
from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from Products.CMFCore.utils import getToolByName

from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic
from emc.kb.portlets import questionportlet


class TestPortlet(unittest.TestCase):

    layer = INTEGRATION_TESTING

    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
#        import pdb
#        pdb.set_trace()
    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='emc.questionportlet')
        self.assertEquals(portlet.addview, 'emc.questionportlet')
    
    def testInterfaces(self):
        portlet = questionportlet.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))
    
    def testInvokeAddview(self):
        portal = self.layer['portal']
        
        portlet = getUtility(IPortletType, name='emc.questionportlet')
        mapping = portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], questionportlet.Assignment))        

    def testRenderer(self):
        
        context = self.layer['portal']
        request = self.layer['request']
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=context)
        assignment = questionportlet.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, questionportlet.Renderer))

class TestRenderer(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
        portal.invokeFactory('emc.kb.topicfolder', 'tf')
        portal['tf'].invokeFactory('emc.kb.topic', 'tc1')       
        portal['tf'].invokeFactory('emc.kb.topic', 'tc2')         
        
        t1=portal['tf']['tc1']
        t2=portal['tf']['tc2']
        
        intids = getUtility(IIntIds)
        portal.invokeFactory('emc.kb.questionfolder','qf')
       
        portal['qf'].invokeFactory('emc.kb.question', 'q1',title='question1',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        
        q1=portal['qf']['q1']
        portal['qf'].invokeFactory('emc.kb.question', 'q2',title='question2',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q3',title='question3',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q4',title='question4',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q5',title='question5',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q6',title='question6',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q7',title='question7',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q8',title='question8',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q9',title='question9',
                                   affiliatedtopics=[RelationValue(intids.getId(t1))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q10',title='question10',
                                   affiliatedtopics=[RelationValue(intids.getId(t2))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q11',title='question11',
                                   affiliatedtopics=[RelationValue(intids.getId(t2))]
                                   )
        portal['qf'].invokeFactory('emc.kb.question', 'q12',title='question12',
                                   affiliatedtopics=[RelationValue(intids.getId(t2))]
                                   )        
                        
        catalog = component.getUtility(ICatalog)
#        import pdb        
#        pdb.set_trace()
        questionlist1 = sorted(catalog.findRelations({'to_id': intids.getId(t1)}))
        questionlist2 = sorted(catalog.findRelations({'to_id': intids.getId(t2)}))
        
        self.assertEqual(9, len(questionlist1))
        self.assertEqual(3, len(questionlist2))

        q2=portal['qf']['q2']
        q2.affiliatedtopics=[RelationValue(intids.getId(t2))]
        event.notify(ObjectModifiedEvent(q2)) 
        questionlist = sorted(catalog.findRelations({'to_id': intids.getId(t2)}))         
        self.assertEqual(4, len(questionlist))

#        t1.relatedtopics = [RelationValue(intids.getId(q1))]
#        t1.relatedtopics[0].from_object = t1
#        q1.affiliatedtopics = [RelationValue(intids.getId(t1))]
#        q1.affiliatedtopics[0].from_object = q1     
#        file = q1         
#        topiclist = list(file.affiliatedtopics)
#        self.assertEqual(1, len(topiclist))
#        self.assertEqual('tc1', topiclist[0].to_object.id)
        
        

    
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        portal = self.layer['portal']
        
        context = context or portal
        request = request or self.layer['request']
        
        view = view or portal.restrictedTraverse('@@plone')
        
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
        assignment = assignment or questionportlet.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
    
    def test_count(self):
        
        portal = self.layer['portal']
        r = self.renderer(context=portal['qf']['q1'], assignment=questionportlet.Assignment(count=10))
        self.assertEqual(8, len([p for p in r.relatedquestions()]))
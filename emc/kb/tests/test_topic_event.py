import unittest
from zope import event
from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility
from plone.uuid.interfaces import IUUID

from emc.kb.events import FollowedEvent
from emc.kb.events import UnFollowedEvent


from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

class TestEvent(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def test_questionfollowed_event(self):
        from emc.kb.contents.question import Iquestion
        from emc.kb.interfaces import IFollowing
        from emc.kb.events import FollowedEvent
        from emc.kb.events import UnFollowedEvent
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.folder', 'folder')
        portal['folder'].invokeFactory('emc.kb.questionfolder', 'questionfolder')
        portal['folder']['questionfolder'].invokeFactory('emc.kb.question', 'question',
                             description=u"discription",
                             additional=u"additional"

                             )
        
        file=portal['folder']['questionfolder']['question']
        
        event.notify(FollowedEvent(file))
        
        mp = getToolByName(portal,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        questionlist = list(userobject.getProperty('myfollow'))

        evlute = IFollowing(file)
        uuid = IUUID(file,None)
        
        self.assertTrue(uuid in questionlist)
        self.assertFalse(evlute.available(username))
        self.assertEqual(1, evlute.followerNum)
        
        event.notify(UnFollowedEvent(file))
        
        mp = getToolByName(portal,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        questionlist = list(userobject.getProperty('myfollow'))
        evlute = IFollowing(file)
        
        self.assertFalse(uuid in questionlist)
        self.assertTrue(evlute.available(username))
        self.assertEqual(0, evlute.followerNum)

    def test_topic_event(self):
        from emc.kb.contents.topic import Itopic
        from emc.kb.interfaces import IFollowing
        from emc.kb.events import FollowedEvent
        from emc.kb.events import UnFollowedEvent
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.folder', 'folder')
        portal['folder'].invokeFactory('emc.kb.topicfolder', 'topicfolder')
        portal['folder']['topicfolder'].invokeFactory('emc.kb.topic', 'topic',
                             name=u"topic",
                             description=u"discription"

                             )
        
        file=portal['folder']['topicfolder']['topic']
        event.notify(FollowedEvent(file))
        
        mp = getToolByName(portal,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        questionlist = list(userobject.getProperty('myfollow'))
        evlute = IFollowing(file)
        uuid = IUUID(file,None)
        self.assertEqual(1, evlute.followerNum)        
        self.assertTrue(uuid in questionlist)
        self.assertFalse(evlute.available(username))
        
        event.notify(UnFollowedEvent(file))
        
        mp = getToolByName(portal,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        questionlist = list(userobject.getProperty('myfollow'))
        evlute = IFollowing(file)
        
        self.assertFalse(uuid in questionlist)
        self.assertTrue(evlute.available(username))
        self.assertEqual(0, evlute.followerNum)
                

           
    def test_repositorytool(self):
        portal = self.layer['portal']
        repository = getToolByName(portal,'portal_repository')
        self.assertTrue('emc.kb.topicfolder' in repository._versionable_content_types)
        self.assertTrue('emc.kb.topic' in repository._versionable_content_types)
        self.assertTrue('emc.kb.questionfolder' in repository._versionable_content_types)
        self.assertTrue('emc.kb.question' in repository._versionable_content_types)
        self.assertTrue('emc.kb.answer' in repository._versionable_content_types)
       
class TestRendering(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
import datetime
import unittest

from plone.testing.z2 import Browser

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD

from plone.app.testing import setRoles

from emc.kb.testing import FUNCTIONAL_TESTING

class TestReservations(unittest.TestCase):

    layer = FUNCTIONAL_TESTING
    
    def setUp(self):
        from emc.kb.mapping_db import Model
        from z3c.saconfig import Session
        
        model = Model()
        model.cinemaCode = u"ABC1"
        model.filmCode = u"DEF1"
        model.showTime = self.checkDate = datetime.datetime.now() + datetime.timedelta(days=1)
        model.remainingTickets = 10
        Session.add(model)
        
        model = Model()
        model.cinemaCode = u"ABC1"
        model.filmCode = u"DEF2"
        model.showTime = datetime.datetime.now() + datetime.timedelta(days=1)
        model.remainingTickets = 10
        Session.add(model)
        
        model = Model()
        model.cinemaCode = u"ABC1"
        model.filmCode = u"DEF2"
        model.showTime = datetime.datetime.now() + datetime.timedelta(days=-1)
        model.remainingTickets = 10
        Session.add(model)
        
        Session.flush()
        
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
        portal.invokeFactory('optilux.CinemaFolder', 'cinemas', title=u"Cinemas")
        
        portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema1',
                title=u"Cinema 1", description=u"First cinema",
                cinemaCode=u"ABC1",
            )
        portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema2',
                title=u"Cinema 2", description=u"Second cinema",
                cinemaCode=u"ABC2",
            )
        
        portal.invokeFactory('optilux.FilmFolder', 'films', title=u"Films")
        
        portal['films'].invokeFactory('optilux.Film', 'film1',
                title=u"Film 1", description=u"First film", filmCode=u"DEF1",
                startDate=datetime.date.today(),
                endDate=datetime.date.today(),
            )
        portal['films'].invokeFactory('optilux.Film', 'film2',
                title=u"Film 2", description=u"Second film", filmCode=u"DEF2",
                startDate=datetime.date.today(),
                endDate=datetime.date.today(),
            )
        
        import transaction; transaction.commit()
    
    def tearDown(self):
        from optilux.cinemacontent.model import Screening
        from z3c.saconfig import Session
        
        # Clean up the database, since we will have made commits above
        
        Session.query(Screening).delete()
        import transaction; transaction.commit()
    
    def test_view_films_at_cinema(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.open(portal['cinemas']['cinema1'].absolute_url())
        
        self.assertEqual(
                browser.getLink('Film 1').url,
                portal['films']['film1'].absolute_url()
            )
        
        self.assertEqual(
                browser.getLink('Film 2').url,
                portal['films']['film2'].absolute_url()
            )
    
    def test_view_cinemas_for_film(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.open(portal['films']['film1'].absolute_url())
        
        self.assertEqual(
                browser.getLink('Cinema 1').url,
                portal['cinemas']['cinema1'].absolute_url()
            )
    
    def test_view_screening(self):
        from Products.CMFCore.utils import getToolByName
        
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.open(portal['cinemas']['cinema1'].absolute_url())
        
        browser.getLink('(show times)', index=0).click()
        
        translation_service = getToolByName(portal, 'translation_service')
        stamp = translation_service.ulocalized_time(
                self.checkDate.isoformat(), 
                long_format=True, 
                context=portal,
                domain='plonelocales',
            )
        
        self.assertTrue(stamp in browser.contents)
    
    def test_make_reservation(self):
        from z3c.saconfig import Session
        from optilux.cinemacontent.model import Screening
        from Products.CMFCore.utils import getToolByName
        
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization',
                'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,)
            )
        
        browser.open(portal['cinemas']['cinema1'].absolute_url())
        browser.getLink('(show times)', index=0).click()
        
        translation_service = getToolByName(portal, 'translation_service')
        stamp = translation_service.ulocalized_time(
                self.checkDate.isoformat(), 
                long_format=True, 
                context=portal,
                domain='plonelocales',
            )
        
        # Go to the reservations page
        browser.getLink(stamp, index=0).click()
        
        browser.getControl('Number of tickets').value = u"2"
        browser.getControl('Customer name').value = u"John Smith"
        browser.getControl('Reserve').click()
        
        # Tickets should now have been reserved
        model = Session.query(Screening) \
                           .filter(Screening.cinemaCode == "ABC1") \
                           .filter(Screening.filmCode == "DEF1") \
                           .first()
        
        self.assertEqual(model.remainingTickets, 8)
        
    def test_cancel_reservation(self):
        from z3c.saconfig import Session
        from optilux.cinemacontent.model import Screening
        from Products.CMFCore.utils import getToolByName
        
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        browser.addHeader('Authorization',
                'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,)
            )
        
        browser.open(portal['cinemas']['cinema1'].absolute_url())
        browser.getLink('(show times)', index=0).click()
        
        translation_service = getToolByName(portal, 'translation_service')
        stamp = translation_service.ulocalized_time(
                self.checkDate.isoformat(), 
                long_format=True, 
                context=portal,
                domain='plonelocales',
            )
        
        # Go to the reservations page
        browser.getLink(stamp, index=0).click()
        
        browser.getControl('Number of tickets').value = u"2"
        browser.getControl('Customer name').value = u"John Smith"
        browser.getControl('Cancel').click()
        
        # No tickets should have been reserved
        model = Session.query(Screening) \
                           .filter(Screening.cinemaCode == "ABC1") \
                           .filter(Screening.filmCode == "DEF1") \
                           .first()
        
        self.assertEqual(model.remainingTickets, 10)

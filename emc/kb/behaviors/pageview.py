#from eisoo.behaviors.pageview import Ipageview
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
#from Products.CMFCore.interfaces import IDublinCore
#from rwproperty import getproperty, setproperty

#from plone.namedfile import field as namedfile
#from z3c.relationfield.schema import RelationChoice, RelationList
#from plone.formwidget.contenttree import ObjPathSourceBinder

from emc.kb import _


class Ipageview(form.Schema):
    """
       Marker/Form interface for pageview
    """
    
    visitnum = schema.Int(
            title=_(u"visitnum"),
            required=True,
            default=0,               
        )
    form.omitted('visitnum')
    # -*- Your Zope schema definitions here ... -*-


alsoProvides(Ipageview,IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)

class pageview(object):
    """
       Adapter for pageview
    """
    implements(Ipageview)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    visitnum = context_property('visitnum')
    
#    implements(Ipageview)
#    adapts(IDublinCore)
#
#    def __init__(self,context):
#        self.context = context
#
#    @getproperty
#    def visitnum(self):
#        return set(self.context.Subject())
#   
#    @setproperty
#    def visitnum(self, value):
#        if value is None:
#            value = ()
#        self.context.setSubject(tuple(value))
    # -*- Your behavior property setters & getters here ... -*-

#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import Interface
from Acquisition import aq_parent, aq_base, Implicit

from emc.kb.interfaces import IVoting
from emc.kb.interfaces import IFollowing

from plone.indexer import indexer
from plone.memoize.instance import memoize
from Products.ZCatalog.interfaces import IZCatalog
from plone.app.textfield import RichText
from plone.directives import dexterity, form
from Products.CMFCore.utils import getToolByName
#from plone.namedfile.field import NamedImage, NamedFile,NamedBlobImage, NamedBlobFile
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.discussion.interfaces import IConversation

from z3c.form import group, field
from z3c.relationfield.schema import RelationList, RelationChoice

from zope import schema
from zope.interface import invariant, Invalid,Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
#viewlet
from Products.Five.browser import BrowserView
from Acquisition import aq_inner
import zope.interface
from plone.app.customerize import registration
from zope.traversing.interfaces import ITraverser,ITraversable
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet
from zExceptions import NotFound
from emc.kb import _

MAX_CONTENT = 200

# Interface class; used to define content-type schema.

class Ianswer(form.Schema):
    """
    answer
    """   

    content = RichText(
            title=_(u"content of the answer"),
            required=True,
        )
    voteNum = schema.Int(
            title=_(u"voteNum"),
            default=0,               
        )
    totalNum = schema.Int(
            title=_(u"totalNum"),
            default=0,
        )
    form.omitted('voteNum','totalNum')


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.


class answer(dexterity.Item):
    grok.implements(Ianswer)
   
    # Add your class methods and properties here

    @form.default_value(field=Ianswer['voteNum'])
    def DefaultvoteNum(data):
    # To get hold of the folder, do: context = data.context
        return 0

#@grok.adapter(Ianswer, name='content')
@indexer(Ianswer)
def content(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``content`` index with the answer .
    """
    pview = context.restrictedTraverse('@@plone')
#    import pdb
#    pdb.set_trace()
    try:
        text = context.content.output
    except:
        text = context.content
        
    if text == None or "":return ""
    croped = pview.cropText(text, MAX_CONTENT)
    if  isinstance(croped, unicode):
        return croped.encode('utf-8')
    return croped


#@grok.adapter(Ianswer, name='voteNum')
@indexer(Ianswer,IZCatalog)
def voteNum(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``voteNum`` index with the answer .
    """
    return IVoting(context).voteNum


#@grok.adapter(Ianswer, name='totalNum')
@indexer(Ianswer,IZCatalog)
def totalNum(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``totalNum`` index with the answer .
    """
    evluate = IVoting(context)
    return evluate.voteNum - len(evluate.disapproved)


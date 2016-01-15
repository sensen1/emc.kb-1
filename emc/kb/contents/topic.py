#-*- coding: UTF-8 -*-
import json
from zope.interface import Interface
from Products.ZCatalog.interfaces import IZCatalog
from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field
from zope.component import getMultiAdapter

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.autocomplete.widget import (
    AutocompleteMultiFieldWidget,
    )

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

# Indexer
from plone.indexer import indexer

from emc.kb import  _

from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope import component
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from emc.kb.contents.answer import Ianswer
# Interface class; used to define content-type schema.

class Itopic(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """
  
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/topic.xml to define the content type
    # and add directives here as necessary.
    
#    form.model("models/topic.xml")
    id = schema.ASCII(
       title=_(u"topic id"),
    )
    name = schema.TextLine(
        title=_(u"topic name"),
        description=_(u"content of name"),
    )
    discription = schema.TextLine(
        title=_(u"topic discription"),
        description=_(u"content of discription"),
    )
    topicpic = NamedBlobImage(
        title=_(u"topic picture"),
        description=_(u"topic picture"),
        required=False,        
    )

    relatedquestion = RelationList(
        title=_(u"topic relatedquestion"),
        description=_(u"content of relatedquestion"),
        value_type=RelationChoice(
                source=ObjPathSourceBinder(portal_type='emc.kb.question'                        
                    ),
            ),
        required=False,
    )
    followernum = schema.Int(
        title=_(u"topic followernum"),
        description=_(u"content of followernum"),
        default=0,
    )

    topicscore = schema.Float(
        title=_(u"topic topicscore"),
        description=_(u"content of topicscore"),
        default=0.0,
    )
    form.omitted('id','followernum','relatedquestion','topicscore')

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
     
class topic(dexterity.Item):
    grok.implements(Itopic)
    
    fields = field.Fields(Itopic)
    fields['relatedquestion'].widgetFactory = AutocompleteMultiFieldWidget    # Add your class methods and properties here


  

    
@grok.adapter(Itopic, name='name')
@indexer(Itopic)
def name(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``name`` index with the topic .
    """
    return context.name

@grok.adapter(Itopic, name='followernum')
@indexer(Itopic,IZCatalog)
def followernum(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``name`` index with the topic .
    """
    return IFollowing(context).followernum

@indexer(Itopic,IZCatalog)
def topicscore(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``totalNum`` index with the answer .    """
    
    return context.topicscore



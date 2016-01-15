from five import grok
from plone.directives import dexterity, form
from plone.memoize.instance import memoize

from zope import schema
from Products.CMFCore.utils import getToolByName
from emc.kb import  _
from emc.kb.contents.topic import Itopic


# Interface class; used to define content-type schema.

class Itopicfolder(form.Schema):
    """
    topic folder
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/topicfolder.xml to define the content type
    # and add directives here as necessary.




class topicfolder(dexterity.Item):
    grok.implements(Itopicfolder)
    
    # Add your class methods and properties here




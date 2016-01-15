#-*- coding: UTF-8 -*-
from five import grok
from zope import event,schema
from plone.directives import dexterity, form
from emc.kb import _

# Interface class; used to define content-type schema.

class Iquestionfolder(form.Schema):
    """
    Description of the Example Type
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/questionfolder.xml to define the content type
    # and add directives here as necessary.

#    form.model("models/questionfolder.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class questionfolder(dexterity.Item):
    grok.implements(Iquestionfolder)
    
    # Add your class methods and properties here



#
        
#-*- coding: UTF-8 -*-
from five import grok
from zope import event,schema
from zope.interface import invariant, Invalid,Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from datetime import datetime

from z3c.form import validator
from z3c.form import group, field
from z3c.form import form, field, button, interfaces
from z3c.relationfield.schema import RelationList, RelationChoice

from plone.indexer import indexer
from plone.app.textfield import RichText
from plone.memoize.instance import memoize
from plone.directives import dexterity, form
from Products.CMFCore.utils import getToolByName

from plone.dexterity.utils import createContentInContainer
#from plone.namedfile.interfaces import IImageScaleTraversable

#from Products.CMFPlone.interfaces import INonStructuralFolder
from plone.formwidget.autocomplete.widget import AutocompleteMultiFieldWidget
from plone.formwidget.contenttree import ContentTreeFieldWidget,ObjPathSourceBinder
#from plone.namedfile.field import NamedBlobImage, NamedBlobFile,NamedImage, NamedFile

from emc.kb.contents.topic import Itopic
# Indexer
from emc.kb import _

# Interface class; used to define content-type schema.
class Iquestion(form.Schema):
    """
    Description of the Example Type
    """   



    affiliatedtopics =  RelationList(
        title=_(u"affiliated topics"),
        description=_(u"affiliated topics(optional)"),
        value_type=RelationChoice(
                source=ObjPathSourceBinder(
                        object_provides=Itopic.__identifier__
                    ),
            ),
        required=False,
        )
   
    followernum = schema.Int(
        title=_(u"question followernum"),
        description=_(u"content of followernum"),
        default=0,
    )

    form.omitted('followernum')

class ValidateSchemaLength(validator.SimpleFieldValidator):
    """Validate the max-length of the description is 300. 
    """
    
    def validate(self, value):
        # Perform the standard validation first
        super(ValidateSchemaLength, self).validate(value)
#        import pdb
#        pdb.set_trace()
        context=self.context
        try:
            des = context.description
            length=len(context.description)
            if length > 300:
                raise Invalid(_(u"the max-length of the description is 300"))            
            
        except:
            pass      

           
# validator.WidgetValidatorDiscriminators(
#         ValidateSchemaLength,
#         field=Iquestion['description'],
#     )
# grok.global_adapter(ValidateSchemaLength)

class question(dexterity.Item):
    grok.implements(Iquestion)
    fields = field.Fields(Iquestion)
    fields['affiliatedtopics'].widgetFactory = AutocompleteMultiFieldWidget
    
    # Add your class methods and properties here



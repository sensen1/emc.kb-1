#-*- coding: UTF-8 -*-
from five import grok
from plone.directives import dexterity, form
from zope import schema
from z3c.form import group, field
from emc.kb import  _

# Interface class; used to define content-type schema.

class Ifeed(form.Schema):
    """
    My followed message
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/feed.xml to define the content type
    # and add directives here as necessary.
    

    type = schema.Int(
        title=_(u"feed message type"),
        description=_(u"feed message type"),
        
    )
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class feed(dexterity.Item):
    grok.implements(Ifeed)
    """
    一个id字段 ascii，存放对应问题的id;
    一个type字段int，存放来源问题的类型：
    1 -话题下新增问题
    2 - 话题下新增回答
    3 - 问题下新增回答
    """
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# feed_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

# class SampleView(grok.View):
#     grok.context(Ifeed)
#     grok.require('zope2.View')
    
    # grok.name('view')
    
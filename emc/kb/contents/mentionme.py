#-*- coding: UTF-8 -*-
from five import grok
from plone.directives import dexterity, form
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import invariant, Invalid

from emc.kb.contents.question import Iquestion

from z3c.form import group, field
from z3c.relationfield.schema import RelationList, RelationChoice

from Products.CMFCore.utils import getToolByName

from emc.kb import _


# Interface class; used to define content-type schema.

class Imentionme(form.Schema):
    """由subscribers 创建该类 对象，为便于索引，类型字段用默认的title字段代替,answer id用description来代替。
    类型字段包括，一：我的提问有新答案；二：我关注的问题有新答案；
        三：有人赞同我的答案；分别用：“1”，“2”，“3”来代替。"""

    questionuid = schema.ASCII(
        title=_(u"mentionme question"),
    )
#     answerid = schema.ASCII(
#         title=_(u"mentionme answerid"),
#     )
    answeruser = schema.TextLine(
        title=_(u"user Id"),
        description=_(u"the user"),
    )

    form.omitted('questionuid')
#    form.model("models/mentionmefolder.xml")

    


class mentionme(dexterity.Item):
    grok.implements(Imentionme)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# mentionmefolder_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.
# grok.templatedir('templates')
# class View(grok.View):
#     grok.context(Imentionme)
#     grok.template('question_view')    
#     grok.require('zope2.View')    
#    grok.name('view')

       
    
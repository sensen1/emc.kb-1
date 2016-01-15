# -*- coding: utf-8 -*-
from Acquisition import aq_base, aq_inner

import time

from datetime import datetime
from DateTime import DateTime

from urllib import quote as url_quote

from zope.i18n import translate
from zope.i18nmessageid import Message
from plone.dexterity.utils import createContentInContainer
from zope.component import createObject, queryUtility

from zope.interface import alsoProvides

from z3c.form import form, field, button, interfaces
from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.registry.interfaces import IRegistry

from plone.app.layout.viewlets.common import ViewletBase

from emc.kb.interfaces import Iaddanswer

from emc.kb import  _

from plone.z3cform import z2
from plone.z3cform.widget import SingleCheckBoxWidget
from plone.z3cform.fieldsets import extensible

from plone.z3cform.interfaces import IWrappedForm

class AnswerForm(extensible.ExtensibleForm, form.Form):
    ignoreContext = True # don't use context to get widget data
    id = None
    label = _(u"Add an answer")
    fields = field.Fields(Iaddanswer).omit('id',
                                           'voteNum',
                                           'totalNum',
                                           )
    
    def updateWidgets(self):
        super(AnswerForm, self).updateWidgets()
        self.widgets['content'].rows = 3
        self.widgets['content'].autoresize = True
    
    def updateActions(self):
        super(AnswerForm, self).updateActions()
        self.actions['answer'].addClass("context")

    @button.buttonAndHandler(_(u"add_answer_button", default=u"Answer"),
                             name='answer')
    
    def handleAnswer(self, action):
        context = aq_inner(self.context)
        
        # Validation form
        data, errors = self.extractData()
        if errors:
            return       
        # Create answer
#         answer = createObject('emc.kb.answer')      

        
#         content = data["content"]
        date = datetime.now()
        id = str(date.year)+str(date.month)+str(date.day)+str(date.hour)+str(date.minute)+str(date.second)
        answer = createContentInContainer(context,"emc.kb.answer",checkConstraints=False,id=id)
        # Set answer attributes
        for attribute in self.fields.keys():
            setattr(answer, attribute, data[attribute])
                    
        self.request.response.redirect(self.action)
    
class AddanswerViewlet(ViewletBase):
    
    form = AnswerForm
    index = ViewPageTemplateFile('addanswer.pt')
    
    def update(self):
        super(AddanswerViewlet, self).update()
        self.form = self.form(aq_inner(self.context), self.request)
        alsoProvides(self.form, IWrappedForm)
        self.form.update()
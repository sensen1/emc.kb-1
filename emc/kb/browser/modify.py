import json
from five import grok
from Acquisition import aq_inner
from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic

class ModifyDescription(grok.View):
    """AJAX action for Modifying title & description.
    """
    
    grok.context(Iquestion)
    grok.name('modify-description')
    grok.require('zope2.View')
        
    def render(self):
        context = aq_inner(self.context)
        data = self.request.form
        description = {'description':context.setDescription(data['description'])}
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(description)

class ModifyTitle(grok.View):
    """AJAX action for Modifying title & description.
    """
    
    grok.context(Iquestion)
    grok.name('modify-title')
    grok.require('zope2.View')
        
    def render(self):
        context = aq_inner(self.context)
        data = self.request.form
        title = {'title':context.setTitle(data['title'])}
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(title)
    
class ModifyDiscription(grok.View):
    """AJAX action for Modifying title & description.
    """
    
    grok.context(Itopic)
    grok.name('modify-discription')
    grok.require('zope2.View')
        
    def render(self):
        context = aq_inner(self.context)
        data = self.request.form
        context.discription = data['discription']
        discription = {'discription':data['discription']}
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(discription)
#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import Interface
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from emc.project.browser.ajax_listing import ajaxListingView
from emc.project.browser.ajax_listing import ajaxsearch
from emc.kb import  _
from emc.kb.contents.topic import Itopic
from emc.kb.contents.topicfolder import Itopicfolder
from emc.kb.contents.questionfolder import Iquestionfolder

grok.templatedir('templates')
class View(ajaxListingView):
    grok.context(Itopicfolder)
    grok.template('ajax_listings')
    grok.require('zope2.View')
    grok.name('ajax_listings')
    
    def canbeRead(self):
#        status = self.workflow_state()
# checkPermission function must be use Title style permission
#         canbe = self.pm().checkPermission(viewReport,self.context)

        return True
    
    
class QuestionfolderView(View):
    grok.context(Iquestionfolder)
    grok.template('ajax_listings')
    grok.require('zope2.View')
    grok.name('ajax_listings')

class KBajaxsearch(ajaxsearch):
    """AJAX action for search.
    """    
    grok.context(Interface)
    grok.name('kbajaxsearch')
    grok.require('zope2.View')
    
    def render(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"ajax_listings")        
 # datadic receive front ajax post data       
        datadic = self.request.form
#         import pdb
#         pdb.set_trace()
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
#         securitykey = int(datadic['security'])  #密级属性：公开/内部/机密
#         tasktypekey = int(datadic['type']) #任务类型属性：分析/设计/实验/仿真/培训 
#         tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = searchview.getPathQuery()
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

#         if securitykey != 0:
#             origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)           
#         if tasktypekey != 0:
#             origquery['task_type'] = searchview.getTaskType(tasktypekey)
#         all = u"所有".encode("utf-8")
# #         import pdb
# #         pdb.set_trace()
#         if tag !=all and tag !="0":
#             rule = {"query":tag,"operator":"or"}
#             origquery['Subject'] = rule
                      
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)    
                
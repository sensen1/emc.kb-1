#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import Interface
from Acquisition import aq_parent, aq_base, Implicit

from plone.memoize.instance import memoize

from Products.CMFCore.utils import getToolByName
#from plone.namedfile.field import NamedImage, NamedFile,NamedBlobImage, NamedBlobFile
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.discussion.interfaces import IConversation
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

from emc.kb.interfaces import IVoting
from emc.kb.interfaces import IFollowing
from emc.memberArea.interfaces import IFavoriting
from emc.kb.contents.answer import Ianswer
from emc.kb import _


class IView(Interface):
    """ answer view interface"""
    def GetMyInfo(self):
        """根据自己的相关信息，包括包含链接，描述，头像"""

    def fetchvotelist(self):
        """最近的三个投票者的名字"""
            
grok.templatedir('templates')
from emc.kb.browser.question import View as baseview
class View(baseview):
    grok.context(Ianswer)
    grok.template('answer_view')
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        """
        """
        # Hide the editable-object border
        self.request.set('disable_border', True)
        questionobject = aq_parent(self.context)
        answerlist = self.catalog()({'object_provides': Ianswer.__identifier__,
                              'path': dict(query='/'.join(questionobject.getPhysicalPath()),
                                      depth=1),
                             'sort_on': 'sortable_title'})
        self.answerNum = len(answerlist)
        self.parentQuestion = questionobject
        self.parenturl = questionobject.absolute_url()
        self.answerdate = self.context.created().strftime('%Y-%m-%d')

    @memoize
    def pm(self):
        context = aq_inner(self.context)
        return getToolByName(context,'portal_membership')    
    @memoize
    def catalog(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        return catalog 
    
    def isTopicpicAvalable(self,topic=None):
        """判断图片字段是否有效"""
        try:
            if topic is None:
                image = self.context.topicpic.size
            else:
                 image = topic.getObject().topicpic.size
                 
            if image != 0:
                return True
            else:
                return False
        except:
            return False
    def getcommentnum(self):
        """获取答案直接评论"""
        conversation = IConversation(self.context)
        return conversation.total_comments
     
    @memoize
    def isFollowed(self):
        """判断当前问题是否已被当前用户关注,返回boolean"""
        obj = (self.context).getParentNode()
        aobj = IFollowing(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = self.pm().getAuthenticatedMember()
        userid = userobject.getId()        
        return aobj.available(userid)

    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj    
    @memoize            
    def isfavorited(self):
        """判断当前答案是否已被收藏,返回boolean"""
        obj = self.context
        aobj = IFavoriting(obj)
        
        userobject = self.pm().getAuthenticatedMember()
        userid = userobject.getId()          
        return aobj.favavailable(userid)
    
   
    @memoize
    def GetCreatorInfo(self,answerid):
        """根据答案id，提取该答案作者的相关信息，包括包含链接，描述，头像"""
        
        query = dict(object_provides=Ianswer.__identifier__,id=answerid)
        # to do using index replace getObject
        answerobject = self.catalog()(query)[0].getObject()
        
        author = answerobject.Creator()
        userobject=self.pm().getMemberById(author)
        username = userobject.getProperty('fullname')
        if username =="":username= author
        authorinfo = {}
        try:
            authorinfo['username'] = username
            authorinfo['homepage'] = userobject.getHomeUrl(userobject.getId()) + '/workspace/feedsfolder'
            authorinfo['description'] = userobject.getProperty('description')
            authorinfo['portrait'] = userobject.getPersonalPortrait(userobject.getId())
        except:
            authorinfo = {'username':'testuser','homepage':'http://test.com/',
                          'description':'test','portrait':'defaultUser.png'}
        return authorinfo
    
    @memoize
    def fetchvotelist(self,size=3):
        """最近的三个投票者的名字"""
        evlute = IVoting(self.context)
        
        votedict = [] 
        if size=='all':
            for ete in evlute.approved:
                userobject=self.pm().getMemberById(ete)
                username = userobject.getProperty('fullname')
                if username =="":username = ete
                votedict.append(username)
        else:
            if evlute.voteNum < size:
                for ete in evlute.approved:
                    userobject=self.pm().getMemberById(ete)
                    username = userobject.getProperty('fullname')
                    if username =="":username = ete
                    votedict.append(username)
            else:
                i = 0
                for ete in evlute.approved:
                    userobject=self.pm().getMemberById(ete)
                    username = userobject.getProperty('fullname')
                    if username =="":username = ete
                    votedict.append(username)
                    i = i + 1
                    if i >= size:
                        break
        return list(votedict)
  
# support template file load viewlet by viewlet name.      
    def __getitem__(self,name):
        viewlet = self.setUpViewletByName(name)
        if viewlet is None:
            active_layers = [ str(x) for x in self.request.__provides__.__iro__]
            active_layers = tuple(active_layers)
            raise ViewletNotFoundException("Viewlet does not exist by name %s for the active theme "% name)
        viewlet.update()
        return viewlet.render()
    
    def getViewletByName(self,name):
        views = registration.getViews(IBrowserRequest)
        for v in views:
            if v.provided == IViewlet:
                if v.name == name:
                    if str(v.required[1]) == '<InterfaceClass plone.app.discussion.interfaces.IDiscussionLayer>':
                        return v
        return None
    
    def setUpViewletByName(self,name):
        context = aq_inner(self.context)
        request = self.request
        reg = self.getViewletByName(name)
        if reg == None:
            return None
        factory = reg.factory
        try:
            viewlet = factory(context,request,self,None).__of__(context)
        except TypeError:
            raise RuntimeError("Unable to initialize viewlet %s. Factory method %s call failed."% name)
        return viewlet

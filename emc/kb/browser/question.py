#-*- coding: UTF-8 -*-
from five import grok
import zope.interface
from Acquisition import aq_inner
from rwproperty import getproperty, setproperty
from plone.app.customerize import registration
from zope.traversing.interfaces import ITraverser,ITraversable
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet
from zExceptions import NotFound

from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope import component
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from plone.app.discussion.interfaces import IConversation
from plone.uuid.interfaces import IUUID
from zope.security import checkPermission
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.instance import memoize


from emc.kb.contents.topic import Itopic
from emc.kb.contents.answer import Ianswer
from emc.kb.interfaces import IVoting
from emc.kb.interfaces import IFollowing
from emc.memberArea.interfaces import IFavoriting
from emc.kb.events import CountNumEvent
from emc.kb.events import FollowedEvent,UnFollowedEvent
from emc.kb import  _
from emc.kb.contents.topic import Itopic
from emc.kb.contents.question import Iquestion

class Iquestionview(zope.interface.Interface):
    
    def fetchAllAnswers(self):
        """获取问题的所有答案，返回字典值，包含id,answerer，content，date，voteNum，voters"""

    def GetAuthorInfoAnswer(id):
        """根据答案id获取作者相关信息，包括包含用户名，链接，描述，头像"""
    
    def GetUserInfo(self):
        """获取当前用户相关信息，包括包含用户名，描述，头像"""
        
        
grok.templatedir('templates')
class View(grok.View):
    grok.context(Iquestion)
    grok.template('question_view')
    grok.require('zope2.View')
    grok.name('view')
    
    def update(self):
        """
        """
        # Hide the editable-object border
        self.request.set('disable_border', True)
        self.answerNum = len(self.fetchAllAnswers())

    @memoize
    def canEdit(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)
    
    @memoize
    def pm(self):
        context = aq_inner(self.context)
        return getToolByName(context,'portal_membership')    
    @memoize
    def catalog(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        return catalog 

    def fetchRelatedTopics(self,questionobj=None):
        """获取问题questionobj的相关话题，返回一个话题对象列表"""
        intids = getUtility(IIntIds)
        if  questionobj == None:questionobj = self.context 
        intid = intids.getId(questionobj)
        catalog = component.getUtility(ICatalog)        
        qlist = sorted(catalog.findRelations({'from_id': intid}))
#         import pdb
#         pdb.set_trace()
        if len(qlist) ==0:return []
        qlists = []
        for q in qlist:
            if not q.to_object is None:
                qlists.append(q.to_object) 
        re = sorted(qlists,key=lambda x:x.modified(),reverse=True)
        return re
    
    def isFollowed(self):
        """判断当前话题是否已被关注,返回boolean"""
        obj = self.context
        aobj = IFollowing(obj)        
        userobject = self.pm().getAuthenticatedMember()
        userid = userobject.getId()
        return aobj.available(userid)

    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj
                
    def fetchAllAnswers(self):
        """获取问题的所有答案，返回字典值，包含id, content，voteNum, date, answerer"""      
        
        answerlist = self.catalog()({'object_provides': Ianswer.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'totalNum',
                             'path': '/'.join(self.context.getPhysicalPath())
                             })
        if len(answerlist) == 0:
            return []
        """先票数后时间排序"""
        re = sorted(answerlist,key=lambda x:(x.totalNum,x.modified),reverse=True)
        return re
        
    def getcommentnum(self,brain = None):
        """获取问题直接评论"""
        if brain is None:
            conversation = IConversation(self.context)
        else:
            conversation = IConversation(brain.getObject())
        return conversation.total_comments
    
    def fetchvotelist(self,answerid,size=3):
        """获取当前赞同到用户"""
         
        obrain = self.catalog()({'object_provides': Ianswer.__identifier__,
                             'id': answerid
                             })
        if len(obrain)==0:return
        obj = obrain[0].getObject()
        evlute = IVoting(obj)
        votedict = []
        
        if size == 'all':
            for ete in evlute.approved:
                userobject = self.pm().getMemberById(ete)
                username = userobject.getProperty('fullname')
                if username =="":username = ete
                votedict.append(username)
        else:
            if evlute.voteNum < size:
                for ete in evlute.approved:
                    userobject = self.pm().getMemberById(ete)
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

    def GetUserInfo(self):
        """获取当前用户相关信息，包括包含用户名，描述，头像"""
        
        userobject = self.pm().getAuthenticatedMember()
        username = userobject.getProperty('fullname')
        userid = userobject.getId()
        if username =="":username = userid
        authorinfo = {}             
        try:
            authorinfo['username'] = username
            authorinfo['homepage'] = userobject.getHomeUrl(userid) + '/workspace/feedsfolder'
            authorinfo['description'] = userobject.getProperty('description')
            authorinfo['portrait'] = userobject.getPersonalPortrait(userid)
        except:
            authorinfo = {'username':'testuser','homepage':'http://test.com/',
                          'description':'test','portrait':'defaultUser.png'}
        return authorinfo
   
   
    def GetAuthorInfoAnswer(self,answerid):
        """根据答案id获取作者相关信息，包括包含链接，描述，头像"""
         
        query = dict(object_provides=Ianswer.__identifier__,id=answerid)
        answerobject = self.catalog()(query)[0].getObject()
        pm = getToolByName(answerobject, 'portal_membership')
        author = answerobject.Creator()
        userobject = self.pm().getMemberById(author)
        username = userobject.getProperty('fullname')
        if username == "": username = author
        
        authorinfo = {}
        try:
            authorinfo['username'] = username
            authorinfo['homepage'] = userobject.getHomeUrl(author) + '/workspace/feedsfolder'
            authorinfo['description'] = userobject.getProperty('description')
            authorinfo['portrait'] = userobject.getPersonalPortrait(author)
        except:
            authorinfo = {'username':'testuser','homepage':'http://test.com/',
                          'description':'test','portrait':'defaultUser.png'}
        return authorinfo

    def isfavorited(self,answer):
        """提供答案的brain,判断当前答案是否已被收藏,返回boolean"""
        obj = answer.getObject()
        aobj = IFavoriting(obj)
        
        userobject = self.pm().getAuthenticatedMember()
        userid = userobject.getId()
        return aobj.favavailable(userid)
    
    def QuestionfollowedNum(self,questionid):
        """获取问题关注人数"""
        
        question = self.catalog()({'object_provides':Iquestion.__identifier__,
                      'id': questionid
                         })
        aobj = IFollowing(question[0].getObject())
        return aobj.followerNum
    
    def Questionisfollowed(self,question):
        """判断当前问题是否已被关注,返回boolean"""
        obj = question.getObject()
        aobj = IFollowing(obj)
        
        userobject = self.pm().getAuthenticatedMember()
        userid = userobject.getId()
        return aobj.available(userid)
    
    def QuestionAnswerNum(self,questionid):
        """获取话问题数量"""
        
        question = self.catalog()({'object_provides':Iquestion.__identifier__,
                            'id': questionid
                         })
        answerlist = self.catalog()({'object_provides':Ianswer.__identifier__,
                          'sort_order': 'reverse',
                         'sort_on': 'voteNum',
                         'path': '/'.join(question[0].getObject().getPhysicalPath())
                         })
        return len(answerlist)
    
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
    
    def traverse(self,name,further_path):
        viewlet = self.setUpViewletByName(name)
        if viewlet is None:
            raise NotFound("Viewlet does not exist by name %s for theme layer %s" % name)
        viewlet.update()
## 接受表单数据
#        
#    def receive(self):
#        data = self.request.form
#        for paremeter in data.keys() :
#            if data[paremeter] == "" or len(data[paremeter]) == 0:
#                data.pop(paremeter)
#        return data
#
#    def container(self):
#        return self.context
#    
#    def create(self,data):
#        folder = self.container()
#        if len(data)<3:
#           self.request.response.redirect(self.context.absolute_url())
#        else:
#            content = data["form.textbox"]
#            date = datetime.now()
#            id = str(date.year)+str(date.month)+str(date.day)+str(date.hour)+str(date.minute)+str(date.second)
#            answer = createContentInContainer(folder,"emc.kb.answer",checkConstraints=False,id=id,content=content)
#            answer.content = content
#            answer.reindexObject()        
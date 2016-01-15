#-*- coding: UTF-8 -*-
from zope.interface import Interface
import json
from five import grok
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName
from Acquisition import aq_parent, aq_base, Implicit
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser

from emc.kb.contents.answer import Ianswer
from emc.kb.contents.topic import Itopic
from emc.kb.interfaces import IVoting

class Imyfavoritefolder(Interface):
    """
    myfavoritefolder view interface 取消收藏事件的绑定是：.unfavorite_answer-favorite a:click
    """

    def haveFavorites():
        """判断当前用户是否至少有一个收藏，返回布尔值"""
#    def GetSpecificQuestion(answerid):
#        """根据答案id,获取答案相关的问题，返回一个字典，
#        包括问题id，
#        问题标题
#        问题绝对路径
#        该问题的相关话题，
#        """
    
    def GetSpecificUser(answer_brain):
        """
        提供一个答案对象的brain，先获得该brain的对象的作者，然后获取该作者相关用户属性，返回一个字典，包含全名，id,绝对网址，描述，头像
        """
    def fetchAllFavorite(start=0, size=10):
        """ 提取当前用户所有收藏的答案，返回一个brain list，要求可以和分页的batch模板配合，按答案的赞成投票数排序，
        每个brain将有如下被调用的metadata(通过索引提供）：
        答案内容，
        答案标题
        答案作者id
        投票数
         """
    def fetchparentquestion(answer_brain): 
         """
         提供一个答案对象的brain，返回该答案的父对象（问题对象）的如下属性：
         id,
         title
         absolute_url
         affiliatedtopics         
         """          
grok.templatedir('templates')
class myfavoritefolder(grok.View):
    grok.context(INavigationRoot)
    grok.template('favoritefolder_view')    
    grok.require('zope2.View')
    grok.name('myfavoritefolder')
    
    def update(self):
        """Called before rendering the template for this view
        """
        # Hide the editable-object border
        self.request.set('disable_border', True)
        self.favoriteNum = len(self.fetchAllFavorite())
        self.haveFavorite = bool((self.favoriteNum)>0)
    
    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj

    
    def fetchParentProperty(self,brain):
        """提供一个brain参数，获取父亲对象的标题和url"""
        obj = brain.getObject().getParentNode()
        pty = {}
        pty['title'] = obj.title
        pty['url'] = obj.absolute_url()
        return pty

    def isfavorited(self,brain):
        """提供答案的brain,判断当前答案是否已被收藏,返回boolean"""
        obj = brain.getObject()
        aobj = IVoting(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()
        return aobj.favavailable(userid)
        
    @memoize
    def fetchAllFavorite(self,start=0,size=10):
        """Get all child cinema folders in this cinema folder.
        
        We memoize this using @plone.memoize.instance.memoize so that even
        if it is called more than once in a request, the calculations are only
        performed once.
        """
        
        catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_state = getMultiAdapter((self.context, self.request),name=u"plone_portal_state",)
        userobject = self.portal_state.member()
        favoritelist = userobject.getProperty('myfavorite')

        if size==0:  
            answerlist = catalog({'object_provides': Ianswer.__identifier__,
                     'id': favoritelist,
                     'sort_order': 'reverse',
                     'sort_on': 'modified'})       
        else:   
            answerlist = catalog({'object_provides': Ianswer.__identifier__,
                                 'id': favoritelist,
                                 'sort_order': 'reverse',
                                 'sort_on': 'modified',
                                 'b_start': start,
                                 'b_size': size})
        return answerlist
      
    def GetSpecificQuestion(self,answerid):
        
        catalog = getToolByName(self.context, 'portal_catalog')
        answerobject = catalog({'object_provides': Ianswer.__identifier__,
                             'id': answerid,
                             'sort_on': 'sortable_title'})
        question = answerobject[0].getObject().getParentNode()
        return [dict(
                    id=question.getId(),
                    geturl=question.absolute_url(),
                    affiliatedtopics=question.affiliatedtopics,
                    title=question.title)
                    ]
        
    def GetSpecificUser(self,voterid):
        pm = getToolByName(self.context,'portal_membership')
        userobject = pm.getMemberById(voterid)
        return dict(
                    username = userobject.getId(),
                    id=userobject.getId(),
                    geturl=userobject.getHomeUrl(userobject.getId()),
                    image=userobject.getPersonalPortrait(userobject.getId()),
                    description=userobject.getProperty('description'))
        
class favoritemore(grok.View):
    """AJAX action for updating ratings.
    """
    
    grok.context(INavigationRoot)
    grok.name('favoritemore')
    grok.require('zope2.View')            
    
    def render(self):

        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst)*3 
        nextstart = formstart+3                
        favorite_view = getMultiAdapter((self.context, self.request),name=u"myfavoritefolder")
        favoritenum = len(favorite_view.fetchAllFavorite(0,0))
        
        if nextstart>=favoritenum :
            ifmore =  1
        else :
            ifmore = 0
            
        braindata = favorite_view.fetchAllFavorite(formstart, 3)
        
        # Capture a status message and translate it
        translation_service = getToolByName(self.context, 'translation_service')        
        
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            question = favorite_view.fetchParentProperty(braindata[i])
            questionUrl = question['url']
            questionTitle = question['title']
            questionTitle = questionTitle.encode('utf-8')
            voteNum = braindata[i].voteNum
            userid = braindata[i].Creator
            userinfo = favorite_view.GetSpecificUser(userid)
            userpage = userinfo['geturl']
            username = userinfo['username']
            userdescription = userinfo['description']
            userdescription = userdescription.encode('utf-8')
            userimage = userinfo['image']
            answerid = braindata[i].id
            answerCon = braindata[i].content
            answerUrl = braindata[i].getURL()          
            favorite = favorite_view.isfavorited(braindata[i])
            if favorite:
                favoritestyle1 = "display:none;"
                favoritestyle2 = "display:inline;"
            else:
                favoritestyle1 = "display:inline;"
                favoritestyle2 = "display:none;"
                            
            out = """<div class="qbox hrtop">
                        <div class="boxTitle">
                            <a href="%s">%s</a>
                        </div>
                        <div class="boxBody">
                            <div class="boxBodyLeft"><span>%s</span></div>
                            <div class="boxBodyRight">
                                <div class="author">
                                    <a href="%s">%s</a><span>,</span>
                                    <span class="description">%s</span>
                                    <span class="littleAvatar">%s</span>
                                </div>
                                <div class="content">%s</div>
                                <div class="more">
                                    <a href="%s">显示全部</a>
                                </div>
                                <div class="favorite_answer-favorite" id="favorite_answer-favorite-%s" style="%s">
                                <a href="#" class="kssattr-answerid-%s">收藏</a>
                                </div>
                                <div class="favorite_answer-unfavorite" id="favorite_answer-unfavorite-%s" style="%s">
                                    <a href="#" class="kssattr-answerid-%s">取消收藏 </a>
                                </div>
                            </div>
                        </div>
                    </div>"""%(questionUrl,questionTitle,voteNum,userpage,username,userdescription,userimage,answerCon,answerUrl,answerid,favoritestyle1,answerid,answerid,favoritestyle2,answerid)
            
            outhtml =outhtml+out
            
        data = {                
            'outhtml': outhtml,
            'ifmore':ifmore,
         }
    
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
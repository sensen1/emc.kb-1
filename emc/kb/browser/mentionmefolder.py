#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from emc.kb.contents.answer import Ianswer
from emc.kb.contents.question import Iquestion
from emc.kb.contents.mentionme import Imentionme
from emc.kb.contents.mentionmefolder import Imentionmefolder
from emc.kb import _

class Imentionmefolderview(Interface):
    """view interface"""
    def Ifetchmentionme(self):
        """ 返回四类信息，一：我的提问有新答案；二：我关注的问题有新答案；
        三：有人赞同我的答案；四：有人修改我的问题；
        需要一个状态参数（暂定为1，2，3，4）注明信息类别，还需要操作触发者，
        触发时间，问题标题，如果是回答，需要回答内容及回答的赞成数，如果是修改，
        需要修改理由，需要分页，返回为catalog类型 """
        

    def ImentionmeQuesiont(self,questionid):
        """返回指定问题基本信息返回catalog类型"""
    
    def ImentionmeAnswer(self,answerid):
        """返回指定答案基本信息返回dict类型,title,voteNum"""
        
    def ImentionmeAnsweruser(self,answerid):
        """返回指定答案用户到基本信息返回dict类型,username,homepage,description,portrait"""
        
    def Imentionmefollowedquestion(self,questionid):
        """指定问题是否已被关注 true 是,false 否"""  
grok.templatedir('templates')
class View(grok.View):
    grok.context(Imentionmefolder)
    grok.template('mentionmefolder_view')
    grok.require('zope2.View')
    grok.name('view')
    
    def update(self):
#         Hide the editable-object border
        self.request.set('disable_border', True)

    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj

    def fetchmentionme(self,start = 0,size = 10):
        """ 返回四类信息，一：我的提问有新答案；二：我关注的问题有新答案；三：有人赞同我的答案；四：有人修改我的问题；
            需要一个状态参数（暂定为1，2，3，4）注明信息类别，还需要操作触发者，触发时间，问题标题，如果是回答，需要回答内容及回答的赞成数，如果是修改，需要修改理由，需要分页，返回为catalog类型 """
        
        mp = getToolByName(self.context,'portal_membership')
        userobject= mp.getAuthenticatedMember()
        url = mp.getHomeUrl(userobject.getId())
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog({'object_provides': Imentionme.__identifier__,
                                 'path': dict(query='/'.join(self.context.getPhysicalPath()),depth=1),
                                 'sort_order': 'reverse',
                                 'sort_on': 'Date',
                                 'b_start': start,
                                 'b_size': size})
            
    def mentionmeQuesiton(self,questionid):
        """返回指定问题基本信息返回catalog类型"""
        self.portal_state = getMultiAdapter((self.context, self.request),name=u"plone_portal_state",)
        userobject = self.portal_state.member()
        catalog = getToolByName(self.context, 'portal_catalog')
        
        return  catalog({'object_provides': Iquestion.__identifier__,
                             'id': questionid,
                             'sort_on': 'sortable_title'})
        
    def mentionmeAnswer(self,answerid):
        """返回指定问题基本信息返回dict类型,title,voteNum"""
        catalog = getToolByName(self.context, 'portal_catalog')
        answerobject=catalog({'object_provides': Ianswer.__identifier__,
                                    'id':answerid,
                                 'sort_on': 'sortable_title'})
        return dict(
                     content = answerobject[0].content,
                     voteNum = answerobject[0].voteNum
                     )
        
    def mentionmeAnsweruser(self,answerid):
        """返回指定答案用户到基本信息返回dict类型,username,homepage,description,portrait"""
#        import pdb
#        pdb.set_trace()
        catalog = getToolByName(self.context, 'portal_catalog')
        answerobject=catalog({'object_provides': Ianswer.__identifier__,
                                    'id':answerid,
                                 'sort_on': 'sortable_title'})
        if len(answerobject)==0: return
        question = answerobject[0].getObject().getParentNode()
     
        question_view = getMultiAdapter((question, self.request),name=u"view")
        return question_view.GetAuthorInfoAnswer(answerid)
    
    def mentionmefollowedquestion(self,questionid):
        """指定问题是否已被关注 true 是,false 否"""
        mp = getToolByName(self.context,'portal_membership')
        userobject= mp.getAuthenticatedMember()
        questionlist = list(userobject.getProperty('myfollow'))
        if questionid in questionlist:
            return True
        return False
#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize

from emc.kb.contents.answer import Ianswer
from emc.kb.contents.question import Iquestion
from emc.kb.contents.mentionme import Imentionme
from emc.kb.contents.mentionmefolder import Imentionmefolder
from emc.kb import _

class Imentionmefolderview(Interface):
    """view interface"""
    def Ifetchmentionme(self):
        """ 返回三类信息，一：我的提问有新答案；二：我关注的问题有新答案；
        三：有人赞同我的答案；
        需要一个状态参数（暂定为1，2，3）注明信息类别，还需要操作触发者，
        触发时间，问题标题，如果是回答，需要回答内容及回答的赞成数，如果是修改，
        需要修改理由，需要分页，返回为catalog类型 """
        

    def ImentionmeQuesiont(self,questionuid):
        """返回指定问题基本信息返回catalog类型"""
    
    def ImentionmeAnswer(self,answeruid):
        """返回指定答案基本信息返回dict类型,title,voteNum"""
        
    def ImentionmeAnsweruser(self,answeruid):
        """返回指定答案用户到基本信息返回dict类型,username,homepage,description,portrait"""
        
    def Imentionmefollowedquestion(self,questionuid):
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
    
    @memoize
    def catalog(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog

    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj

    def fetchmentionme(self,start = 0,size = 10):
        """ 返回四类信息，一：我的提问有新答案；二：我关注的问题有新答案；三：有人赞同我的答案；
            需要一个状态参数（暂定为1，2，3，）注明信息类别，还需要操作触发者，触发时间，问题标题，如果是回答，需要回答内容及回答的赞成数，如果是修改，需要修改理由，需要分页，返回为catalog类型 """
        

        
        return self.catalog()({'object_provides': Imentionme.__identifier__,
                                 'path': dict(query='/'.join(self.context.getPhysicalPath()),depth=1),
                                 'sort_order': 'reverse',
                                 'sort_on': 'Date',
                                 'b_start': start,
                                 'b_size': size})
            
    def mentionmeQuesiton(self,questionuid):
        """返回指定问题基本信息返回catalog类型"""

        
        
        return  self.catalog()({'object_provides': Iquestion.__identifier__,
                             'UID': questionuid,
                             'sort_on': 'sortable_title'})
        
    def mentionmeAnswer(self,answeruid):
        """返回指定答案基本信息返回dict类型,title,voteNum"""
        
        answerobject=self.catalog()({'object_provides': Ianswer.__identifier__,
                                    'UID':answeruid,
                                 'sort_on': 'sortable_title'})
        return dict(
                     content = answerobject[0].content,
                     voteNum = answerobject[0].voteNum
                     )
        
    def mentionmeAnsweruser(self,answeruid):
        """返回指定答案用户到基本信息返回dict类型,username,homepage,description,portrait"""
#        import pdb
#        pdb.set_trace()
        
        answerobject=self.catalog()({'object_provides': Ianswer.__identifier__,
                                    'UID':answeruid,
                                 'sort_on': 'sortable_title'})
        if len(answerobject)==0: return
        question = answerobject[0].getObject().getParentNode()
     
        question_view = getMultiAdapter((question, self.request),name=u"view")
        return question_view.GetAuthorInfoAnswer(answeruid)
    
    def getUrlByid(self,questionuid):
        
        qbrain = self.catalog()({'object_provides': Iquestion.__identifier__,
                                    'UID':questionuid,
                                 'sort_on': 'sortable_title'})
        return qbrain[0].getURL()        
        
    def mentionmefollowedquestion(self,questionuid):
        """指定问题是否已被我关注 true 是,false 否"""
        mp = getToolByName(self.context,'portal_membership')
        userobject= mp.getAuthenticatedMember()
        questionlist = list(userobject.getProperty('myfollowquestion'))
      
        if questionuid in questionlist:
            return True
        return False
#-*- coding: UTF-8 -*-
from five import grok
from emc.memberArea.browser.contents_view import FavoriteListView
from plone.app.layout.navigation.interfaces import INavigationRoot

grok.templatedir('templates') 
class FollowListView(FavoriteListView):
     "emc memberArea todo listing view"
     
     grok.context(INavigationRoot)
     grok.template('Ifollowed')
     grok.name('followed')
     grok.require('zope2.View')
     
     def getFavoriteItemsId(self):
         userobject = self.pm().getAuthenticatedMember()
         fwlist = list(userobject.getProperty('myfollow'))
         return fwlist
     
     def outputList(self,braindata):
        """ output brains for template render
        """
        outhtml = ""
        brainnum = len(braindata)
        obj = self.context
      
        for i in braindata:
            objurl =  i.getURL()           
            id = i.id
            uid = i.UID            
            name = i.Title # message object's title
            description = i.Description
            sender = i.Creator
            register_date = i.created.strftime('%Y-%m-%d')
#             status = i.review_state                          
                        
            out = """<tr class="row">
                  <td class="col-md-8">
                      <a href="%(url)s">
                         <span>%(name)s</span>
                      </a>
                  </td>                
                  <td class="col-md-2 text-left">%(register_date)s
                  </td>
                  <td class="col-md-2 unfollow" rel="%(uid)s" data-ajax-target="%(url)s">
                  <a href="#" class="link-overlay btn btn-danger">
                                      <i class="icon-trash icon-white"></i>取消关注</a>
                  </td>""" % dict(url=objurl,name=name,uid=uid,register_date=register_date)                 
                                     
         
            outhtml = "%s%s" %(outhtml,out)
        return outhtml           
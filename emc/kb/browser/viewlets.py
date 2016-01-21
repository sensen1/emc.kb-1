# encoding=utf-8
from plone.app.layout.viewlets import common as base
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import getToolByName
from emc.kb import DoFollow,DoVote
from emc.kb.interfaces import IFollowing
from emc.kb.interfaces import IVoting


class Follow(base.ViewletBase):

    follow = None
    is_manager = None
    can_follow = None

    # Update methods are guaranteed to be called before rendering for
    # Viewlets and Portlets (Because they are IContentProvider objects)
    # and for z3c.forms and formlib forms. But *not* for normal Browser Pages
    def update(self):
        super(Follow, self).update()

        if self.follow is None:
            self.follow = IFollowing(self.context)

        if self.is_manager is None:
            self.pm = getToolByName(self.context, 'portal_membership')
            self.is_manager = self.pm.checkPermission(
                ViewManagementScreens, self.context)
            self.can_follow = self.pm.checkPermission(
                DoFollow, self.context)

    def Isfollowed(self):
        "是否已被当前用户关注"
        userid = self.pm.getAuthenticatedMember().getId()
        return (self.follow.available(userid))

class Vote(base.ViewletBase):

    voteAdapter = None
    is_manager = None
    can_vote = None

    # Update methods are guaranteed to be called before rendering for
    # Viewlets and Portlets (Because they are IContentProvider objects)
    # and for z3c.forms and formlib forms. But *not* for normal Browser Pages
    def update(self):
        super(Vote, self).update()

        if self.voteAdapter is None:
            self.voteAdapter = IVoting(self.context)

        if self.is_manager is None:
            self.pm = getToolByName(self.context, 'portal_membership')
            self.is_manager = self.pm.checkPermission(
                ViewManagementScreens, self.context)
            self.can_follow = self.pm.checkPermission(
                DoVote, self.context)

    def voteavailableapproved(self):
        "是否当前用户在赞成队列，true:已在队列中"
        userid = self.pm.getAuthenticatedMember().getId()
        return not(self.voteAdapter.voteavailableapproved(userid))

    def voteavailabledisapproved(self):
        "是否当前用户在反对队列，true:已在队列中"
        userid = self.pm.getAuthenticatedMember().getId()
        return not(self.voteAdapter.voteavailabledisapproved(userid))
    def voteNum(self):
        "当前对象赞成总票数"
        return self.voteAdapter.voteNum
        

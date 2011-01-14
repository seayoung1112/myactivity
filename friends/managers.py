from django.conf import settings
from django.db import models
from django.db.models import Q

class FriendshipManager(models.Manager):
    
    def friends_for_user(self, user):
        friends = []
        qs = self.filter(Q(from_user=user) | Q(to_user=user)).select_related(depth=1)
        for friendship in qs:
            if friendship.from_user == user:
                friends.append({"friend": friendship.to_user, "friendship": friendship})
            else:
                friends.append({"friend": friendship.from_user, "friendship": friendship})
        return friends
    
    def are_friends(self, user1, user2):
        return self.filter(
            Q(from_user=user1, to_user=user2) |
            Q(from_user=user2, to_user=user1)
        ).count() > 0
    
    def remove(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            friendship = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            friendship = self.filter(from_user=user2, to_user=user1)
        friendship.delete()



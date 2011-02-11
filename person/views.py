from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from user_activity.models import Invite, Activity
from friends.models import FriendInvitation
from profile.models import UserTag
from story.models import StoryInvitation
from django.contrib.auth.models import User

@login_required
def home(request):
    user = request.user
    public_activities = Activity.objects.filter(is_public=True, state='P')
    #user.ac_invitee.filter(id__in=Invite.objects.filter(user=user).exclude(response='U').values_list('activity')).order_by('start_time')[:1]
    activities_created = user.ac_invitor.all().order_by('start_time')[:1]
    stories = list(user.stories_created.all()) + list(user.stories_participated.all())
    activity_invitation = Invite.objects.filter(user=user, response='U')
    story_invitation = StoryInvitation.objects.filter(to_user=user)
    friend_application_count = FriendInvitation.objects.filter(to_user=user).count()
    return render_to_response('user/index.html', {'user': user, 'activities_created': activities_created,
                                                  'public_activities': public_activities,   
                                                  'activity_invitation': activity_invitation,
                                                  "story_invitation": story_invitation,
                                                  'friend_application_count': friend_application_count,
                                                  'stories': stories,
                                                  },
                                                  context_instance=RequestContext(request))

def search(request):
    username = request.GET['user_name']
    template = request.GET.get('template', None)
    users = User.objects.filter(profile__real_name__icontains=username)
    if template is None:
        return HttpResponse("no template!")
    return render_to_response(template, {'users': users,},
                              context_instance=RequestContext(request))
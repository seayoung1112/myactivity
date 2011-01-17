from django.shortcuts import render_to_response, redirect
from accounts.forms import UserRegisterForm
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from forms import SuggestionForm
from helper import send_mail
from user_activity.models import Invite
from friends.models import FriendApplication
from profile.models import UserTag
from story.models import StoryInvitation

def index(request):
    if request.user.is_authenticated():
        return redirect('/home/')
    reg_form = UserRegisterForm()
    log_form = AuthenticationForm()
    return render_to_response('home/index.html', {'reg_form': reg_form, 'log_form': log_form,}, 
                              context_instance=RequestContext(request))
    
@login_required
def home(request):
    user = request.user
    activities_invited = user.ac_invitee.filter(id__in=Invite.objects.filter(user=user).exclude(response='U').values_list('activity')).order_by('start_time')[:1]
    activities_created = user.ac_invitor.all().order_by('start_time')[:1]
    stories = list(user.stories_created.all()) + list(user.stories_participated.all())
    activity_invitation = Invite.objects.filter(user=user, response='U')
    story_invitation = StoryInvitation.objects.filter(to_user=user)
    friend_application_count = FriendApplication.objects.filter(apply_object=user).count()
    hot_tags = UserTag.objects.all()
    return render_to_response('user/index.html', {'user': user, 'activities_created': activities_created,
                                                  'activities_invited': activities_invited,   
                                                  'activity_invitation': activity_invitation,
                                                  "story_invitation": story_invitation,
                                                  'friend_application_count': friend_application_count,
                                                  'stories': stories,
                                                  'hot_tags': hot_tags,},
                                                  context_instance=RequestContext(request))

@login_required
def suggest(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            send_mail(request.user.profile.real_name + 'report',
                      form.cleaned_data['description'],
                      request.user.email,
                      ['seayoung1112@gmail.com',])
            return render_to_response('home/suggest_suc.html')
    form = SuggestionForm()
    return render_to_response('home/suggest.html', {'form': form,},
                              context_instance=RequestContext(request))
    
def contact(request):
    return render_to_response('home/contact.html')

def updates(request):
    return render_to_response('home/updates.html')

def about(request):
    return render_to_response('home/about.html')
from django.contrib.auth.decorators import login_required
from forms import StoryForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import Story
from friends.models import friend_set_for
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.

@login_required
def create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():       
            story = form.save(False)
            story.creator = request.user
            story.save()
            return redirect('/story/edit/' + str(story.id))

            
    else:
        form = StoryForm()
    return render_to_response('story/create.html', {'form': form,}, 
                              context_instance=RequestContext(request))

@login_required   
def edit(request, story_id):#only the invitor can modify it
    user = request.user
    story = Story.objects.get(id=story_id)
    if story.creator == user:
        if request.method == 'POST':
            form = StoryForm(request.POST, instance=story)
            if form.is_valid():            
                form.save()
        else:
            form = StoryForm(instance=story)
        participant_set = set(story.participants.all())
        all_users = set(User.objects.exclude(id=user.id).exclude(is_staff=True).filter(privacy__allow_stranger_invite = True)) - participant_set
        friends = friend_set_for(user) - participant_set        
        return render_to_response('story/edit.html', {'form': form, 'story_id': story_id, 
                                                         'friends': friends, 'participants': story.participants.all(),
                                                         'all_users': all_users,
                                                         'invite_action': '/story/invite/'+story_id+'/'},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse('you are not permit to do this!')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from profile.models import Profile, User
from models import FriendApplication, Friendship
from django.template import RequestContext
from django.http import HttpResponse

def search(request):
    username = request.GET['user_name']
    user_profiles = Profile.objects.filter(real_name=username)
    return render_to_response('friends/search.html', {'user_profiles': user_profiles,},
                              context_instance=RequestContext(request))
    
@login_required
def add(request, user_id):
    friend = User.objects.get(id=user_id)
    FriendApplication.objects.get_or_create(applicant=request.user, apply_object=friend)
    return redirect('/home')

@login_required
def application(request):
    applications = FriendApplication.objects.filter(apply_object=request.user)
    return render_to_response('friends/application.html', {'friend_applications': applications})

@login_required
def agree(request, app_id):
    application = FriendApplication.objects.get(id=app_id)
    if request.user != application.apply_object:
        return HttpResponse("you are not permitted to do this!")
    friendship = Friendship.objects.get_or_create(to_user=application.applicant, from_user=application.apply_object)
    if friendship is not None:
        application.delete()
    return redirect('/friends/application')
    
@login_required
def ignore(request, app_id):
    application = FriendApplication.objects.get(id=app_id)
    if request.user != application.apply_object:
        return HttpResponse("you are not permitted to do this!")
    application.delete()
    return redirect('/friends/application')
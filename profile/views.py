from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist 
from models import UserTag
from forms import ProfileEditForm, Profile
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

@login_required
def edit(request):
    try:
        profile = request.user.get_profile()
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:          
                form.save()
            except:
                return HttpResponse('save failed!')
            return HttpResponseRedirect('/home/')
    else:
        form = ProfileEditForm(instance=profile)
    hot_tags = UserTag.objects.all()
    return render_to_response('profile/edit.html', {'form': form, 
                                                    'hot_tags': hot_tags,},
                              context_instance=RequestContext(request))

@login_required
def add_tag(request, tag_id=None):
    tag_name = ""
    if request.method == "POST":
        tag_name = request.POST.get('tag_name', default=None)
        tag_id = request.POST.get('tag_id', default=None)
    request.user.profile.add_tag(tag_name=tag_name, tag_id=tag_id)
    return redirect('/profile/edit')
    
@login_required
def remove_tag(request, tag_id):
    request.user.profile.remove_tag(tag_id=tag_id)
    return redirect('/profile/edit')
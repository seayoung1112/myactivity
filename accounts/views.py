# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from forms import UserRegisterForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from privacy.models import Privacy

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                                    email=form.cleaned_data['username'], 
                                                    password=form.cleaned_data['password'])
                
            except:
                return render_to_response('accounts/register.html', {'form': form,}, 
                              context_instance=RequestContext(request))
            Privacy.objects.create(user=new_user)
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
            return HttpResponseRedirect('/profile/edit')
    else:
        form = UserRegisterForm()
    return render_to_response('accounts/register.html', {'form': form,}, 
                              context_instance=RequestContext(request))
            
            
        
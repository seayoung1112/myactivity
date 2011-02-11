# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from forms import UserRegisterForm
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from privacy.models import Privacy
import uuid

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                try:
                    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                                        email=form.cleaned_data['username'], 
                                                        password=form.cleaned_data['password'], 
                                                        )
                    
                except Exception as e:
                    return HttpResponse(str(e))
                Privacy.objects.create(user=new_user)
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    login(request, user)
                return redirect('/profile/edit')
            form.errors.add({"password": "password does not match"})
        form.errors.add({"all": "form not valid"})
    else:
        form = UserRegisterForm()
    return render_to_response('accounts/register.html', {'form': form,}, 
                              context_instance=RequestContext(request))
            
            
def check_user_exist(request, email):
    if User.objects.filter(username = email).exists():
        return HttpResponse(True)
    return HttpResponse(False)
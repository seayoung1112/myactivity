# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from forms import UserRegisterForm
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from privacy.models import Privacy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import get_current_site
from django.conf import settings
from profile.models import Profile
import re
import uuid

@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- redirects to http://example.com should
            # not be allowed, but things like /view/?param=http://example.com
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)

    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)
    

    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

def register(request):
    redirect_to = request.REQUEST.get('next', '')
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
                Profile.objects.create(user=new_user)
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    auth_login(request, user)
                if not redirect_to or ' ' in redirect_to:
                    redirect_to = '/profile/edit'
                return redirect(redirect_to)
            form.errors["password"] = "password does not match"
        form.errors["all"] = "form not valid"
    else:
        form = UserRegisterForm()
    return render_to_response('accounts/register.html', {'form': form,
                                                         'next': redirect_to}, 
                              context_instance=RequestContext(request))
            
            
def check_user_exist(request, email):
    if User.objects.filter(username = email).exists():
        return HttpResponse(True)
    return HttpResponse(False)

@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/person/settings')
    else:
        form = PasswordChangeForm(user=request.user)
    return render_to_response('accounts/change_password.html', {
        'form': form,
    }, context_instance=RequestContext(request))
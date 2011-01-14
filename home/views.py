from django.shortcuts import render_to_response, redirect
from accounts.forms import UserRegisterForm
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from forms import SuggestionForm
from helper import send_mail

def index(request):
    if request.user.is_authenticated():
        return redirect('/home/')
    reg_form = UserRegisterForm()
    log_form = AuthenticationForm()
    return render_to_response('home/index.html', {'reg_form': reg_form, 'log_form': log_form,}, 
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
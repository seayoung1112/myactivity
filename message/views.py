# Create your views here.
from models import Message, send_message
from forms import MessageForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
def inbox(request):
    messages =  Message.objects.filter(to_user=request.user)
    return render_to_response('message/inbox.html', {'messages': messages})

def send(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            send_message(from_user=request.user, to_user=form.cleaned_data[''])
            return redirect()
    else:
        form = MessageForm()
    return render_to_response('message/send.html', {'form': form}, 
                              context_instance=RequestContext(request))
    
def sended(request):
    messages =  Message.objects.filter(from_user=request.user)
    return render_to_response('message/sended.html', {'messages': messages})
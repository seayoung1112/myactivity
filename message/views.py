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
            send_message(from_user=request.user, form=form)
            return redirect('/message/sended')
    else:
        form = MessageForm()
    return render_to_response('message/send.html', {'form': form}, 
                              context_instance=RequestContext(request))
    
def sended(request):
    messages =  Message.objects.filter(from_user=request.user)
    return render_to_response('message/inbox.html', {'messages': messages},
                              context_instance=RequestContext(request))

def detail(request, message_id):
    message = Message.objects.get(id=message_id)
    if message.readed == False:
        message.readed = True
        message.save()
    return render_to_response('message/detail.html', {'message':message},
                              context_instance=RequestContext(request))
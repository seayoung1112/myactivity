from models import Privacy
from forms import PrivacyEditForm
from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext

def edit(request):
    try:
        privacy = request.user.privacy
    except ObjectDoesNotExist:
        privacy = Privacy.objects.create(user=request.user)
    if request.method == 'POST':
        form = PrivacyEditForm(request.POST, instance=privacy)
        if form.is_valid():
            try:          
                form.save()
            except:
                return HttpResponse('save failed!')
            return redirect('/privacy/')
    else:
        form = PrivacyEditForm(instance=privacy)

    return render_to_response('privacy/edit.html', {'form': form, },
                              context_instance=RequestContext(request))


from models import Message
from django.forms import ModelForm

class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ('from_user', 'readed', 'type', 'send_time')
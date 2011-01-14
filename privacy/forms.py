from django.forms import ModelForm
from models import Privacy

class PrivacyEditForm(ModelForm):
    class Meta:
        model = Privacy
        exclude = ('user')
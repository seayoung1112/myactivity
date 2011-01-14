from django.forms import ModelForm
from models import Profile

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'tags')
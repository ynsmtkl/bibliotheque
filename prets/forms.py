from django.forms import ModelForm, TextInput, Textarea
from dashboard.models import Livre


class LivrePretForm(ModelForm):
    class Meta:
        model = Livre
        fields = ('titre',)
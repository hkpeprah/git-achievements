from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from app.assets.models import *


class AchievementForm(ModelForm):
    """
    Form for creating/editing achievements.
    """
    class Meta:
        model = Achievement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AchievementForm, self).__init__(*args, **kwargs)

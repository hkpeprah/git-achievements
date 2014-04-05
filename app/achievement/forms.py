from collections import namedtuple
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper

import django.forms as forms
from django.forms.models import inlineformset_factory

from app.assets.models import Achievement, Condition, Badge




class AchievementForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'difficulty', 'achievement_type', 'grouping']
        labels = {
            'name': 'Achievement Name',
            'description': 'Achievement Description',
            'achievement_type': 'Type of Achievement',
            'grouping': 'Condition Grouping'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        """
        @param self: AchievementForm instance
        @param args: List of arguments
        @param kwargs: List of keyword arguments
        @return: AchievementForm
        """
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'achievement-form'
        self.helper.form_action = 'achievement_create'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(AchievementForm, self).__init__(*args, **kwargs)

        Difficulty = namedtuple('Difficulty', ('id', 'name'))

        self.fields['difficulty'].choices = filter(lambda d: not Difficulty(*d).name == "legendary",
            self.fields['difficulty'].choices)


class BadgeForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Badge
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2})
        }


BadgeFormset = inlineformset_factory(Badge, Achievement,
    fields=('name', 'description'), can_delete=False)

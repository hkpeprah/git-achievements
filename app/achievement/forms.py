from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.contenttypes.models import ContentType

from app.achievement.models import *


class AchievementConditionForm(ModelForm):
    class Meta:
        model = AchievementCondition

    def __init__(self, *args, **kwargs):
        super(AchievementConditionForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].choices = (
            (ContentType.objects.get_for_model(ValueCondition), 'Value Condition'),
            (ContentType.objects.get_for_model(AttributeCondition), 'Attribute Condition'),
        )


class AchievementForm(ModelForm):
    """
    Form for creating/editing achievements.
    """
    class Meta:
        model = Achievement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AchievementForm, self).__init__(*args, **kwargs)

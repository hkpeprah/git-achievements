from django.contrib import admin

from apps.assets.models import *


class TitleAdmin(admin.ModelAdmin):
    """
    Admin for Title model.
    """
    pass

admin.site.register(Title, TitleAdmin)


class MethodAdmin(admin.ModelAdmin):
    """
    Admin for creating methods in the administrator
    page.
    """
    pass

admin.site.register(Method, MethodAdmin)


class QualifierAdmin(admin.ModelAdmin):
    """
    Admin for defining qualifiers.
    """
    pass

admin.site.register(Qualifier, QualifierAdmin)


class QuantifierAdmin(admin.ModelAdmin):
    """
    Admin for defining quantifiers.
    """
    pass

admin.site.register(Quantifier, QuantifierAdmin)


class ConditionTypeAdmin(admin.ModelAdmin):
    """
    Admin for defining the type of conditions.
    """
    pass

admin.site.register(ConditionType, ConditionTypeAdmin)


class ConditionAdmin(admin.ModelAdmin):
    """
    Admin for creating Conditions.
    """
    pass

admin.site.register(Condition, ConditionAdmin)


class ConditionInline(admin.TabularInline):
    model = Condition
    extra = 1


class AchievementTypeAdmin(admin.ModelAdmin):
    """
    Admin for defining the types of achievements.
    """
    pass

admin.site.register(AchievementType, AchievementTypeAdmin)


class AchievementAdmin(admin.ModelAdmin):
    """
    Admin for creating achievements.
    """
    inlines = [ConditionInline]

admin.site.register(Achievement, AchievementAdmin)

from django.conf import settings


def hosting_services(request):
    """
    Provides the list of the hosting services that are supported.

    @param request: HttpRequest object
    @return: dict
    """
    return {'HOSTING_API_SERVICES': settings.HOSTING_API_SERVICES}

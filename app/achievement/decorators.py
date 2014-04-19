def check_read_notifications(function):
    """
    Decorator to handle processing notifications passed along by a request

    @param function: function
    @return: function
    """
    def wrap(request, *args, **kwargs):
        """
        Wrapper around the request object.
        """
        if request.user:
            notifications = request.user.notifications

            if request.GET.get('notification', None):
                notification_id = request.GET['notification']
                if notification_id == 'all':
                    notifications.mark_all_as_read(request.user)

                elif len(notifications.filter(id=notification_id)) > 0:
                    notification = notifications.get(id=notification_id)
                    notification.mark_as_read()

                request.GET = request.GET.copy()
                del request.GET['notification']

        return function(request, *args, **kwargs)

    return wrap

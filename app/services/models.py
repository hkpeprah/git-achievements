import jsonfield

from django.db import models


class Event(models.Model):
    """
    An event object stores the name of an event and the structure of the payload,
    and types expected in the payload.
    """
    name = models.CharField(max_length=90)
    service = models.CharField(max_length=90)
    # Stores both the attribute json with sample input
    # and the attribute json with the expected types
    payload = jsonfield.JSONField()
    attributes = jsonfield.JSONField()

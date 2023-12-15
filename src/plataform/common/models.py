from django.db import models
from enum import IntEnum


class Log(models.Model):
    class Status(IntEnum):
        REJECTED = 0
        PENDING = 1
        APPROVED = 2

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    requester_name = models.CharField(max_length=100)
    requester_number = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    quantity = models.IntegerField()
    category = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices(), default=Status.PENDING)
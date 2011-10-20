from django.dispatch import Signal

#Send signal when a beta invite has been used by a newly created user
invite_complete = Signal(providing_args=["user"])
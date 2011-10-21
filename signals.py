from django.dispatch import Signal

#Send signal when a beta invite has been used by a newly created user
invite_used = Signal(providing_args=["user", "invitation_code"])
invite_sent = Signal(providing_args=["email"])
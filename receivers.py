#when user with corresponding email has been created then set the code as used.
def invitation_code_used(sender, user, request, **kwargs):
    try:
        invitation_code = InvitationCode.objects.get(email=user.email)
        invitation_code.user = user
        invitation_code.is_used = True
        invitation_code.used_date = datetime.datetime.now()
        invitation_code.save()
    except InvitationCode.DoesNotExist:
        pass
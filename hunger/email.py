import os.path
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from hunger.utils import setting

def beta_confirm(email, **kwargs):
    """
    Send out email confirming that they requested an invite.
    """

    templates_folder = setting('BETA_EMAIL_TEMPLATES_DIR', 'hunger')
    plaintext = get_template(os.path.join(templates_folder, 'beta_confirm.txt'))
    html = get_template(os.path.join(templates_folder, 'beta_confirm.html'))

    from_email = setting('EMAIL_HOST_USER')
    subject, to = 'You requested an invite!', email
    text_content = plaintext.render(Context())
    html_content = html.render(Context())
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to],
                                 headers={'From': 'Mailer <%s>' % from_email})
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def beta_invite(email, code, **kwargs):
    """
    Email for sending out the invitation code to the user.
    Invitation code is added to the context, so it can be rendered with standard
    django template engine.
    """
    context_dict = kwargs.copy()
    context_dict.setdefault('code', code)
    context = Context(context_dict)

    templates_folder = setting('BETA_EMAIL_TEMPLATES_DIR', 'hunger')
    plaintext = get_template(os.path.join(templates_folder, 'beta_invite.txt'))
    html = get_template(os.path.join(templates_folder, 'beta_invite.html'))

    from_email = setting('EMAIL_HOST_USER')
    subject, to = "Here is your invite", email
    text_content = plaintext.render(context)
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to],
                                 headers={'From': 'Mailer <%s>' % from_email})
    msg.attach_alternative(html_content, "text/html")
    msg.send()

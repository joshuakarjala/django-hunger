from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def beta_invite(email, code):
    """
    Email for sending out the invitation code to the user.
    Invitation code is added to the context, so it can be rendered with standard django template engine.
    """
    context = Context({'code': code })
    
    plaintext = get_template('mail/beta_invite.txt')
    html = get_template('mail/beta_invite.html')
    
    subject, from_email, to = "Here is you invite", 'hello@webservice.com', email
    text_content = plaintext.render(context)
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], headers={'From': 'Webservice <hello@webservice.com>'})
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def beta_confirm(email):
    """
    Send out confirmation to user that they are on the waiting list to use your service
    """
    plaintext = get_template('mail/beta_confirm.txt')
    html = get_template('mail/beta_confirm.html')
    
    subject, from_email, to = 'You requested an invite!', 'hello@webservice.com', email
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], headers={'From': 'Webservice <hello@webservice.com>'})
    msg.attach_alternative(html_content, "text/html")
    msg.send()
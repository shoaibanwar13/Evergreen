from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_email_to_user(subject, template_path, context, recipient_list):
    html_content = render_to_string(template_path, context)
    text_content = context.get("message", subject)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
 
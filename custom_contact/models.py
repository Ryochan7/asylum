from django.db import models
from django.core.mail import mail_admins
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.core import urlresolvers
from django.conf import settings
from contact_form.models import Feedback

def contact_email_admins (sender, instance, created, raw, **kwargs):
    send = getattr (settings, "CONTACT_SEND_ADMIN_MAIL", False)
    edit_url = url = urlresolvers.reverse ("admin:contact_form_feedback_change",
            args=(instance.id,))
    if created and not raw and send:
        subject = render_to_string (
            "contact_form/contact_form_subject_admin.txt",
            {}
        )
        message = render_to_string (
            "contact_form/contact_form_admin.txt",
            {"feedback": instance, "edit_url": edit_url}
        )
        mail_admins (subject, message)

post_save.connect (contact_email_admins, sender=Feedback)


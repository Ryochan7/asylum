from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


from djangobb_forum.signals import post_saved, topic_saved
from djangobb_forum.models import Post, Topic
from .signals import post_saved as custom_post_saved

# Create your models here.
post_save.disconnect(receiver=post_saved, sender=Post,
    dispatch_uid='djangobb_post_save')
#post_save.disconnect(receiver=topic_saved, sender=Topic)

post_save.connect(custom_post_saved, sender=Post, dispatch_uid='djangobb_post_save')


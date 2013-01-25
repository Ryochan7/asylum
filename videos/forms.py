import re
import logging
from django import forms
from .models import Video

logger = logging.getLogger ("videos.forms") 

class VideoOptions (forms.Form):
    autoplay = forms.BooleanField (initial=False)


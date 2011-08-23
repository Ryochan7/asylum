# Create your models here.
from django.db import models
from treemenus.models import MenuItem

class MenuItemExtension(models.Model):
    menu_item = models.OneToOneField (MenuItem, related_name="extension")
    #published = models.BooleanField (default=True)
    protected = models.BooleanField (default=False)
    css_classes = models.TextField (blank=True, default="",
        help_text="Specify additional css classes to use for menu item"
    )


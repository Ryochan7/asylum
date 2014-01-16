import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.db.models.signals import pre_save, post_save, post_delete

from mezzanine.core.fields import FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.core.models import (Displayable, RichText, Slugged,
    TimeStamped, Orderable)


class Platform(Slugged):
    icon = FileField(verbose_name=_("Platform Icon"),
        upload_to=upload_to("gameprofiles.Platform.icon", "uploads/platformicons"), format="Image", max_length=255)


    class Meta(object):
        verbose_name = _("Platform")
        verbose_name_plural = _("Platforms")


class Application(Displayable, RichText, AdminThumbMixin):
    platforms = models.ManyToManyField(Platform)
    boxart = FileField(verbose_name=_("Box Art"),
        upload_to=upload_to("gameprofiles.Application.boxart", "uploads/application/boxart"), format="Image", max_length=255)

    admin_thumb_field = "boxart"

    @models.permalink
    def get_absolute_url(self):
        return ("profiles_details", (), {"slug": self.slug})

    def has_gamecontroller_profile(self):
        return (self.profile_set.filter(controller__guid=Controller.GAMECONTROLLER_GUID)
            ).count() > 0
    
    has_gamecontroller_profile.boolean = True
    has_gamecontroller_profile.short_description = "GameController Support"


class Screenshot(Orderable, TimeStamped, AdminThumbMixin):
    application = models.ForeignKey(Application)
    image = FileField(verbose_name=_("Screenshot"),
        upload_to=upload_to("gameprofiles.Screenshot.image", "uploads/gameprofiles/screenshots"), format="Image", max_length=255)


class Controller(models.Model):
    GAMECONTROLLER_GUID = "00000000000000000000000000000000"

    guid = models.CharField(verbose_name=_("GUID"), max_length=64, blank=True, db_index=True)
    name = models.CharField(verbose_name=_("Name"), max_length=100, db_index=True)
    platforms = models.ManyToManyField(Platform, verbose_name=_("Platforms"))

    def __str__(self):
        return u"{} ({})".format(self.name, self.guid)


    def platform_string(self):
        platform_names = [platform.title for platform in self.platforms.all()]
        temp = ", ".join(platform_names)
        return temp
    platform_string.short_description = "Platforms"


    def filtered_guid(self):
        temp = None
        if self.guid is not None and self.guid != GAMECONTROLLER_GUID:
            temp = self.guid
        return temp


class Profile(TimeStamped, RichText):
    author = models.CharField(verbose_name=_("Author"), max_length=200)
    file = FileField(verbose_name=_("Game Profile"),
        upload_to=upload_to("gameprofiles.Profile.file", "uploads/gameprofiles/profiles"), extensions=[".xml"], max_length=255)
    download_count = models.PositiveIntegerField(default=0, editable=False)
    controller = models.ForeignKey(Controller)
    application = models.ForeignKey(Application)

    def __str__(self):
        return "{} ({}) - {}".format(self.application.title, self.controller.name, self.author)

    @property
    def calculate_download_count(self):
        return ProfileDownload.objects.filter(profile__exact=self).count()


class ProfileDisplayUser(Profile):
    """
    Use this to change the display string for profiles
    used in FeaturedProfileInline.
    """

    class Meta(object):
        proxy = True

    def __str__(self):
        return "{} - {} ({})".format(self.author, self.application.title, self.controller.name)


class FeaturedProfile(models.Model):
    application = models.OneToOneField(Application)
    profile = models.OneToOneField(ProfileDisplayUser)

    class Meta(object):
        unique_together=("application", "profile",)
        verbose_name = _("Featured Profile")
        verbose_name_plural = _("Featured Profiles")

    def __str__(self):
        return "{}".format(self.id)


class ProfileDownload(models.Model):
    ipaddress = models.GenericIPAddressField(verbose_name=_("IP Address"))
    profile = models.ForeignKey(Profile)
    accessed = models.DateTimeField(verbose_name=_("Accessed"), default=datetime.datetime.now)

    class Meta(object):
        unique_together = ("ipaddress", "profile",)

    def __str__(self):
        return "{} - {}".format(self.ipaddress, self.profile_id)


def update_profile_download_count(sender, instance, **kwargs):
    if instance.id:
        # Instance is being updated. Grab original object from
        # database.
        old_profile_download = ProfileDownload.objects.get(pk=instance.id)
        if instance.profile_id != old_profile_download.profile_id:
            # Linked profile is different. Update download count on
            # old profile object.
            new_download_count = old_profile_download.profile.calculate_download_count - 1
            new_download_count = new_download_count if new_download_count > 0 else 0
            old_profile_download.profile.download_count = new_download_count
            old_profile_download.profile.save(update_fields=["download_count"])

def new_profile_download_count(sender, instance, created, **kwargs):
    # Update download count for currently linked profile.
    new_download_count = instance.profile.calculate_download_count
    instance.profile.download_count = new_download_count
    instance.profile.save(update_fields=["download_count"])

def deleted_profile_download_count(sender, instance, **kwargs):
    # Update profile download count after deleting an entry.
    profile = instance.profile
    new_download_count = profile.calculate_download_count
    profile.download_count = new_download_count
    profile.save(update_fields=["download_count"])

pre_save.connect(update_profile_download_count, sender=ProfileDownload)
post_save.connect(new_profile_download_count, sender=ProfileDownload)
post_delete.connect(deleted_profile_download_count, sender=ProfileDownload)

Application._meta.get_field("slug").db_index = True
Platform._meta.get_field("slug").db_index = True


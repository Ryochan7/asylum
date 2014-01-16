from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin

from .models import (Platform, Application, Controller, Profile,
    FeaturedProfile, Screenshot, ProfileDownload)


class ScreenshotsInline(TabularDynamicInlineAdmin):
    model = Screenshot


class FeaturedProfileInline(TabularDynamicInlineAdmin):
    model = FeaturedProfile
    verbose_name_plural = _("Featured Profile")

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(FeaturedProfileInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "profile":
            if request._obj_ is not None:
                tempobject = request._obj_
                field.queryset = field.queryset.filter(application__exact=tempobject).select_related()
            else:
                field.queryset = field.queryset.none()

        return field


application_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
application_fieldsets[0][1]["fields"].extend(["boxart", "platforms", "content"])

application_list_display = list(DisplayableAdmin.list_display)
application_list_display.insert(0, "admin_thumb")


class ApplicationAdmin(DisplayableAdmin):
    fieldsets = application_fieldsets
    list_display = application_list_display + ["has_gamecontroller_profile"]
    list_select_related = True

    inlines = (ScreenshotsInline, FeaturedProfileInline,)

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        current_form = super(ApplicationAdmin, self).get_form(request, obj, **kwargs)
        current_form.base_fields["title"].label = _("Name")
        return current_form


class PlatformAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ["title", "icon"],
        }),
    )


class ControllerAdmin(admin.ModelAdmin):
    list_display = ["name", "guid", "platform_string"]
    list_filter = ("platforms",)
    search_fields = ("name", "guid",)
    list_select_related = True


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ["application", "controller", "author", "content", "file"],
        }),
    )
    list_display = ["application", "controller", "author", "file"]
    search_fields = ("application__title",)
    date_hierarchy = "created"
    list_select_related = True


    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        print(db_field.name)
        if db_field.name == "application":
            field.queryset = field.queryset.order_by("title")

        return field


class ProfileDownloadAdmin(admin.ModelAdmin):
    search_fields = ("ipaddress",)

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        current_form = super(ProfileDownloadAdmin, self).get_form(request, obj, **kwargs)
        current_form.base_fields["ipaddress"].initial = request.META["REMOTE_ADDR"]
        return current_form

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Controller, ControllerAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileDownload, ProfileDownloadAdmin)


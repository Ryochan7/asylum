from django.contrib import admin
from treemenus.admin import MenuAdmin, MenuItemAdmin
from treemenus.models import Menu
from menu_extension.models import MenuItemExtension
from menu_extension.forms import MenuItemExtensionAdminForm

class MenuItemExtensionInline(admin.StackedInline):
    model = MenuItemExtension
    max_num = 1

class CustomMenuItemAdmin(MenuItemAdmin):
    inlines = [MenuItemExtensionInline,]
    form = MenuItemExtensionAdminForm

class CustomMenuAdmin(MenuAdmin):
    menu_item_admin_class = CustomMenuItemAdmin

admin.site.unregister(Menu) # Unregister the standard admin options
admin.site.register(Menu, CustomMenuAdmin) # Register the new,
                                           # customized, admin options

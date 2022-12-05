from django.contrib import admin
from .models import Item, Inventory

admin.site.register(Item)
admin.site.register(Inventory)
admin.site.site_header = "OLOPSC - Kitchen Inventory Management System"
admin.site.site_title = "KIMS"
from django.contrib import admin
from .models import Saflora_user,Cart,Location,AnonymousUser,Province

admin.site.register(Saflora_user)
admin.site.register(Cart)
admin.site.register(Location)
admin.site.register(AnonymousUser)
admin.site.register(Province)
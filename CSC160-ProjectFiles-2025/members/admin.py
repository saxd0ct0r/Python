from django.contrib import admin
from .models import Members


# Register your models here.


class MembersAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname')


admin.site.register(Members, MembersAdmin)


from django.contrib import admin

# Register your models here.

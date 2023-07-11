from django.contrib import admin
from .models import Test


# Register your models here.
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'succ')


admin.site.register(Test, TestAdmin)

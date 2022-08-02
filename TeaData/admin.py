from django.contrib import admin
from .models import County, City, Person
# Register your models here.

admin.site.register(Person)


class CityInline(admin.TabularInline):
    model = City

class CountyAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name']}),
                 ]
    inlines = [CityInline,]

# admin.site.register(FrontView)
admin.site.register(County, CountyAdmin)
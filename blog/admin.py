from django.contrib import admin
from blog import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Post,PostAdmin)
admin.site.register(models.Tag,TagAdmin)
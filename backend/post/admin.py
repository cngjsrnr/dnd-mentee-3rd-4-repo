from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display=['id','category','title','press']

admin.site.register(Post,PostAdmin)
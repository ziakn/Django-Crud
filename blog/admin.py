from django.contrib import admin
from .models import Post, Profile

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','body','status')
    list_filter = ('title','slug','author','body','status')
    search_fields = ('author__username','title')
    prepopulated_fields={'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')


admin.site.register(Post ,PostAdmin)
admin.site.register(Profile ,ProfileAdmin)

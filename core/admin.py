from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'blockchain_id', 'user', 'caption', 'image', 'created_at', 'tx_hash')
    list_filter = ('created_at',)
    search_fields = ('caption', 'user', 'tx_hash')

admin.site.register(Post, PostAdmin)

admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Profile)
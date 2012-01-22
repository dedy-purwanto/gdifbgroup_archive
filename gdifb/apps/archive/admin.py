from django.contrib import admin

from .models import Member, Post, Like

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id','member_id','name')
    search_fields = ('name',)

admin.site.register(Member, MemberAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id','parent','post_id','member','message','date_added','date_created','date_updated')
    search_fields = ('message',)

admin.site.register(Post, PostAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id','member','post', 'date_created')

admin.site.register(Like, LikeAdmin)

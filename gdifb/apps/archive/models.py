from django.db import models
class Member(models.Model):
    member_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Post(models.Model):
    parent = models.ForeignKey('self', null=True, related_name='comments')
    post_id = models.CharField(max_length=255, unique=True)

    member = models.ForeignKey(Member, related_name='posts')
    message = models.TextField()
    link = models.TextField(blank=True, null=True)
    link_name = models.TextField(blank=True, null=True)
    
    date_added = models.DateTimeField(auto_now_add=True) 
    #FB date and time
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(null=True)

    def __unicode__(self):
        return "%s - %s..." % (self.member.name, self.message[:10])

    class Meta:
        ordering = ('date_created',)

class Like(models.Model):
    post = models.ForeignKey(Post,related_name='likes')
    member = models.ForeignKey(Member,related_name='likes')
    date_created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s - %s..." % (self.member.name, self.post.message[:10])


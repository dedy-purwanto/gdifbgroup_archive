#TODO: convert time from fb to DateTimeField, compare date update of post, if it's new then fetch new comments, or if comment count>0 at the time post is created on db, fetch comments as well
import urllib2
import simplejson

from archive.models import Post, Member
ACCESS_TOKEN = "AAACEdEose0cBAN3v1kTcvd6iye0ddjA0BRiWdiaJfSLCbHo3iciRKIlWvPw4gfuZCrZBweKZB41a50xqIvlmlBXixrpvmfqJmJsR5mn3wZDZD"
BASE_URL = "https://graph.facebook.com"
GROUP_ID = "158948640832279"

def fetch_comments(url):
    pass
def fetch_posts(url=None):
    if not url:
        url = "%s/%s/feed?access_token=%s" % (BASE_URL, GROUP_ID, ACCESS_TOKEN)
    if not url:
        return
    data = urllib2.urlopen(url).read()
    json = simplejson.loads(data)
    posts = json['data']

    for p in posts:
        post_id = p['id'].split('_').pop()
        author = p['from']['name']
        author_id = p['from']['id']
        message = p['message']

        date = p['created_time']
        comment_count = p['comments']['count']
        post_feed_link = "%s/%s?access_token=%s" % (BASE_URL, post_id, ACCESS_TOKEN)
        print ("%s - %s comments: %s") % (author, date, comment_count)

        try:
            member = Member.objects.get(member_id=author_id)
        except Member.DoesNotExist:
            member = Member()
            member.member_id = author_id
            member.name = author
        
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            post = Post()
            post.post_id = post_id
            post.parent = None
            post.member = member
            post.message = message




        

import urllib2
import simplejson
from datetime import datetime

from django.core.management.base import BaseCommand
from archive.models import Post, Member, Like

class Command(BaseCommand):
    #TODO: MOVE all this to settings
    ACCESS_TOKEN = "AAACEdEose0cBAEQMMWHjuz9ORs9NItzrBg1wKEF5PABZCTxS5zFq8VcTXeJy1lMJ0hgJGe5GGvTJ6I6WGPufUDfLIPAm3fvHMilTRXgZDZD"
    BASE_URL = "https://graph.facebook.com"
    GROUP_ID = "158948640832279"

    def convert_fb_time(self, time):
        time = time.split('+').pop(0)
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        return time
    
    def add_member(self, author, author_id):
        try:
            member = Member.objects.get(member_id=author_id)
        except Member.DoesNotExist:
            member = Member()
            member.member_id = author_id
            member.name = author
            member.save()
            self.stdout.write("New member added:%s\n" % member)
        return member

    def add_post(self, post_data, parent=None):
        post_updated = True
        post_id = post_data['id'].split('_').pop()
        author = post_data['from']['name']
        author_id = post_data['from']['id']
        message = post_data['message']

        date_created = self.convert_fb_time(post_data['created_time'])
        date_updated = None
        if 'updated_time' in post_data:
            date_updated = self.convert_fb_time(post_data['updated_time'])

        link = None
        link_name = None
        if 'link' in post_data:
            link = post_data['link']
        if 'link_name' in post_data:
            link_name = post_data['link_name']

        member = self.add_member(author, author_id)

        try:
            post = Post.objects.get(post_id=post_id)
            if date_updated:
                if post.date_updated == date_updated:
                    post_updated = False
            post.date_updated = date_updated
            post.save()
        except Post.DoesNotExist:
            post = Post()
            post.post_id = post_id
            post.parent = parent
            post.member = member
            post.message = message
            post.date_created = date_created
            post.date_updated = date_updated
            if link:
                post.link = link
            if link_name:
                post.link_name = link_name
            post.save()
            self.stdout.write("New post added:%s\n" % post)

        if post_updated and post.parent is None:
            self.fetch_comments_and_likes(post)
            post.date_updated = date_updated
            post.save()

        return post

    def fetch_comments_and_likes(self, post):
        self.stdout.write("Fetching commets for post %s \n" % post.post_id)
        url = "%s/%s?access_token=%s" % (self.BASE_URL, post.post_id, self.ACCESS_TOKEN)
        data = urllib2.urlopen(url).read()
        json = simplejson.loads(data)
        if json['comments']['count'] > 0:
            comments = json['comments']['data']
            for c in comments:
                self.add_post(c, parent=post)

        if 'likes' in json:
            likes = json['likes']['data']
            for like in likes:
                author = like['name']
                author_id = like['id']
                member = self.add_member(author, author_id)
                try:
                    like = Like.objects.get(member=member, post=post)
                except Like.DoesNotExist:
                    like = Like()
                    like.post = post
                    like.member = member
                    like.save()

    def fetch_posts(self, url=None, fetch_everything=False):
        if not url:
            url = "%s/%s/feed?access_token=%s" % (self.BASE_URL, self.GROUP_ID, self.ACCESS_TOKEN)
        if not url:
            return
        data = urllib2.urlopen(url).read()
        json = simplejson.loads(data)
        posts = json['data']

        for p in posts:
            self.add_post(p)
        if fetch_everything:
            if 'paging' in json:
                paging = json['paging']
                next_url = paging.get('next', None)
                if next_url:
                    self.stdout.write("Fetching next: %s" % next_url)
                    self.fetch_post(next_url)


    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching..\n")
        self.fetch_posts()
        self.stdout.write("Done.\n")

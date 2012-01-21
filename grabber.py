#!/usr/bin/python

import urllib2
import simplejson
ACCESS_TOKEN = "AAACEdEose0cBAN3v1kTcvd6iye0ddjA0BRiWdiaJfSLCbHo3iciRKIlWvPw4gfuZCrZBweKZB41a50xqIvlmlBXixrpvmfqJmJsR5mn3wZDZD"
BASE_URL = "https://graph.facebook.com"
GROUP_ID = "158948640832279"

print "grabbing.."

def grabfeed(url):
    url = "%s/%s" % (BASE_URL,url)
    resp=urllib2.urlopen(url)
    page_data=resp.read()
    json = simplejson.loads(page_data)
    return json

#feed_url = "%s/feed?access_token=%s" % (group_id, ACCESS_TOKEN)
#json=grabfeed(feed_url)
#posts = json['data']
#paging = json['paging']
#for idx, p in enumerate(posts):
    #author = p['from']['name']
    #date = p['created_time']
    #comments = p['comments']['data']
    #print '%s at %s with %s comments' % (author, date, len(comments))

#print 'Previous:%s\nNext:%s\n' % (paging['previous'], paging['next'])


#post_url = "276128469114295"
#post = grabfeed(post_url)

#print "From: %s at %s with %s comments of len and %s comments of count" %\
        #(
            #post['from']['name'],
            #post['created_time'],
            #len(post['comments']['data']),
            #post['comments']['count'],
        #)
#fetch comments of individual posts
def batagor(url):
    pass
#main grabber
def mieayam(url=None,offset=0):
    if not url:
        url = "%s/%s/feed?access_token=%s" % (BASE_URL, GROUP_ID, ACCESS_TOKEN)
    if not url:
        return
    data = urllib2.urlopen(url).read()
    json = simplejson.loads(data)
    posts = json['data']
    paging = json['paging']

    for p in posts:
        offset += 1
        post_id = p['id'].split('_').pop()
        author = p['from']['name']
        date = p['created_time']
        comment_count = p['comments']['count']
        post_feed_link = "%s/%s?access_token=%s" % (BASE_URL, post_id, ACCESS_TOKEN)
        #print ("Processing post %s from %s at %s with %s comments:%s") %\
                #(
                    #post_id,
                    #author,
                    #date,
                    #comment_count,
                    #post_feed_link
                #)
        print ("%s. %s - %s comments: %s") % (offset, author, date, comment_count)
    if 'next' in paging:
        url = paging['next']
        print "Fetching next: %s" % url
        mieayam(url, offset)
        
mieayam()

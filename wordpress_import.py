from django.core.management import setup_environ
import settings
import os, sys
from xml.etree import ElementTree as ET

setup_environ (settings)

PROJECT_PATH  = os.path.dirname (__file__)
ROOT_FILE_PATH = os.path.abspath (os.path.join (PROJECT_PATH, '..'))

if ROOT_FILE_PATH not in sys.path:
    sys.path.insert (0, ROOT_FILE_PATH)

if PROJECT_PATH not in sys.path:
    sys.path.insert (1, PROJECT_PATH)

#print sys.path

from django.contrib.auth.models import User
from blog.models import Post
import datetime
import re

youtube_re = re.compile ("\[youtube=http://(?:www\.)?youtube\.com/watch\?v=(\S+)\]")

author = User.objects.get (username="ryochan7")
tree = ET.parse ("/home/ryochan7/webapps/ryochan_asylum/asylum/wordpress.2008-11-08.xml")

for item in tree.findall ("channel/item"):
    if item.find ("{http://wordpress.org/export/1.0/}post_type").text == "post":
        result = {}
        result['title'] = item.find ("title").text
        result['slug'] = item.find ("{http://wordpress.org/export/1.0/}post_name").text
        result['body_raw'] = item.find ("{http://purl.org/rss/1.0/modules/content/}encoded").text

        if youtube_re.search (result['body_raw']):
            result['body_raw'] = re.sub (youtube_re, r'<object type="application/x-shockwave-flash" width="425" height="344" data="http://www.youtube.com/v/\1"><param name="movie" value="http://www.youtube.com/v/\1"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param></object>', result['body_raw'])

        result['pub_date'] = item.find ("{http://wordpress.org/export/1.0/}post_date").text
        result['pub_date'] = datetime.datetime.strptime (result['pub_date'], "%Y-%m-%d %H:%M:%S")
        if result['pub_date'] < datetime.datetime (2008, 01, 01):
            print "You no indexed."
            continue

        result['edit_date'] = result['pub_date']

        if item.find ("{http://wordpress.org/export/1.0/}status").text == "publish":
            result['published'] = True
        else:
            result['published'] = False

        result['tags'] = []
        for category in item.findall ("category"):
#            print category.attrib
            if category.attrib.get ("domain") == "tag" and category.attrib.get ("nicename"):
#                print category.attrib.get ("nicename")
                result['tags'].append (category.attrib.get ("nicename"))

        if result['tags']:
            print result['tags']

        new_post = Post (title=result['title'], slug=result['slug'], body_raw=result['body_raw'],
        pub_date=result['pub_date'], edit_date=result['edit_date'], published=result['published'], tags=' '.join (result['tags']), author=author)
        print new_post
#        new_post.save ()
#        print result


print Post.objects.all ()



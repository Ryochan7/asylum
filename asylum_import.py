from django.core.management import setup_environ
import settings
import os, sys
from xml.etree import ElementTree as ET

setup_environ (settings)

PROJECT_PATH = os.path.dirname (__file__)
ROOT_FILE_PATH = os.path.abspath (os.path.join (PROJECT_PATH, '..'))

if ROOT_FILE_PATH not in sys.path:
    sys.path.insert (0, ROOT_FILE_PATH)

if PROJECT_PATH not in sys.path:
    sys.path.insert (1, PROJECT_PATH)

#print sys.path

import datetime
import re
from urllib2 import urlopen
import urlparse
from tempfile import NamedTemporaryFile
from markdown import markdown

from django.contrib.auth.models import User
from django.utils.timezone import get_current_timezone
from django.core.files import File
from django.core.files.storage import default_storage
from django.core import serializers

from mezzanine.generic.models import AssignedKeyword, Keyword
from mezzanine.blog.models import BlogPost, BlogCategory
from videos.models import Video, VideoCategory
from projects.models import Project, ProjectCategory

author = User.objects.get(username="ryochan7")
tree = ET.parse(os.path.join(PROJECT_PATH, "testdump_full.xml"))

# Convert all taggit tags to instances of Keyword
blog_tags = tree.findall("object[@model='taggit.tag']")
for item in blog_tags:
    tag_title = item.find("field[@name='name']").text
    tag, created = Keyword.objects.get_or_create(title=tag_title)

# Grab and cache association between tags and blog post objects
tag_association = {}
old_tags = tree.findall("object[@model='taggit.taggeditem']")
for tag in old_tags:
    tag_id = tag.find("field[@name='tag']").text
    post_id = tag.find("field[@name='object_id']").text
    #post = tree.find("object[@model='blog.post'][@pk='" + post_id + "']")
    actual_tag = tree.find("object[@model='taggit.tag'][@pk='" + tag_id + "']")
    tag_title = actual_tag.find("field[@name='name']").text
    print "Tag id: " + tag_id
    print "Post id: " + post_id
    if not tag_association.has_key(post_id):
	tag_association[post_id] = []

    tag_association[post_id].append(tag_title)

(blog_cat, created) = BlogCategory.objects.get_or_create(title="blog")

original_blog_posts = tree.findall("object[@model='blog.post']")

for item in reversed(original_blog_posts):
    result = {}
    old_id = item.attrib.get("pk")
    result["title"] = item.find("field[@name='title']").text

    # Convert Markdown text to HTML
    result["content"] = item.find("field[@name='body']").text.strip()
    #result["content"] = item.find("field[@name='body_raw']").text
    #result["content"] = markdown(result["content"])

    # Get around aware datetime object requirement in Django
    result["publish_date"] = item.find("field[@name='pub_date']").text
    result["publish_date"] = datetime.datetime.strptime(result["publish_date"],
	"%Y-%m-%d %H:%M:%S").replace(tzinfo=get_current_timezone())

    result["allow_comments"] = item.find("field[@name='enable_comments']").text
    result["allow_comments"] = True if result["allow_comments"] == "True" else False

    result["status"] = item.find("field[@name='published']").text
    result["status"] = 2 if result["status"] == "True" else 1

    #result["_meta_title"] = ""
    result["featured_image"] = ""
    tag_list = tag_association[old_id] if tag_association.has_key(old_id) else []
    result["keywords_string"] = " ".join(tag_list)

    # Make initial user the author of all blog posts
    result["user"] = author

    #print result

    newpost = BlogPost.objects.create(**result)
    newpost.categories.add(blog_cat)
    print newpost
    for tag in tag_list:
	keyword, created = Keyword.objects.get_or_create(title=tag)
	newpost.keywords.add(AssignedKeyword(keyword=keyword))


original_videos = tree.findall("object[@model='videos.video']")

for item in reversed(original_videos):
    result = {}
    result["title"] = item.find("field[@name='title']").text
    result["content"] = item.find("field[@name='description']").text.strip()

    # Get around aware datetime object requirement in Django
    result["publish_date"] = item.find("field[@name='pub_date']").text
    result["publish_date"] = datetime.datetime.strptime(result["publish_date"],
	"%Y-%m-%d %H:%M:%S").replace(tzinfo=get_current_timezone())

    result["allow_comments"] = False
    result["status"] = 2
    result["video_url"] = item.find("field[@name='video_url']").text

    #result["_meta_title"] = ""

    category = item.find("field[@name='category']").text
    category_name = tree.find("object[@model='videos.videocategory'][@pk='" + category + "']/field[@name='title']").text
    (video_cat, created) = VideoCategory.objects.get_or_create(title=category_name)
    result["category"] = video_cat

    # Get temp version of file
    image_path = item.find("field[@name='photo']").text
    image_url = "http://www.ryochan7.com/media/{0}".format(image_path)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(image_url).read())
    img_temp.flush()
    
    # Get around Filebrowser requirements and save file
    image_filename = os.path.basename(urlparse.urlparse(image_url).path)
    final_path = "uploads/video_images/201301/{0}".format(image_filename)
    uploadedfile = default_storage.save(final_path, File(img_temp))
    result["featured_image"] = uploadedfile # Path relative to MEDIA_ROOT

    # Now object can be created
    newvideo = Video.objects.create(**result)
    print newvideo


original_projects = tree.findall("object[@model='projects.project']")

for item in reversed(original_projects):
    result = {}
    result["title"] = item.find("field[@name='title']").text
    result["content"] = item.find("field[@name='description']").text.strip()
    result["summary"] = item.find("field[@name='summary']").text

    # Get around aware datetime object requirement in Django
    result["begin_date"] = item.find("field[@name='begin_date']").text
    result["begin_date"] = datetime.datetime.strptime(result["begin_date"],
	"%Y-%m-%d").replace(tzinfo=get_current_timezone()).date()

    result["end_date"] = item.find("field[@name='end_date']").text
    result["end_date"] = datetime.datetime.strptime(result["end_date"],
	"%Y-%m-%d").replace(tzinfo=get_current_timezone()).date()
 
    #result["allow_comments"] = False
    result["status"] = 2
    result["url"] = item.find("field[@name='url']").text

    #result["_meta_title"] = ""

    category = item.find("field[@name='ptype']").text
    print category
    category_name = tree.find("object[@model='projects.projecttype'][@pk='" + category + "']/field[@name='name']").text
    print category_name
    (project_cat, created) = ProjectCategory.objects.get_or_create(title=category_name)
    result["category"] = project_cat

    # Get temp version of file
    image_path = item.find("field[@name='picture']").text
    image_url = "http://www.ryochan7.com/media/{0}".format(image_path)
    img_temp = NamedTemporaryFile(delete = True)
    img_temp.write(urlopen(image_url).read())
    img_temp.flush()

    # Get around Filebrowser requirements and save file
    image_filename = os.path.basename(urlparse.urlparse(image_url).path)
    final_path = "uploads/project_images/201301/{0}".format(image_filename)
    uploadedfile = default_storage.save(final_path, File(img_temp))
    result["featured_image"] = uploadedfile # Path relative to MEDIA_ROOT

    newproject = Project.objects.create(**result)
    print newproject



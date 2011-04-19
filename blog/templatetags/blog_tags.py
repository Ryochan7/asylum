from django import template
import re
import datetime
import calendar
import hashlib
from urllib import urlencode
from blog.models import Post

register = template.Library ()

class PostPositionNode (template.Node):
    def __init__ (self, post_object):
        self.unresolved_post = template.Variable (post_object)

    def render (self, context):
        self.current_post = self.unresolved_post.resolve (context)
        post_previous = self.current_post.get_previous_post ()
        post_next = self.current_post.get_next_post ()
        context.update ({'post_previous': post_previous})
        context.update ({'post_next': post_next})
        return u''

def do_get_post_position (parser, token):
    """{% get_post_position post %}"""
    bits = token.contents.split ()
    if len(bits) != 2:
        raise template.TemplateSyntaxError (u"'%s' tag takes two arguments" % bits[0])
    return PostPositionNode (bits[1])

register.tag ('get_post_position', do_get_post_position)

def print_post_date_list ():
    return {'postlist': Post.published_objects.dates ('pub_date', 'month')}

register.inclusion_tag ("blog/templatetags/post_date_listing.html")(print_post_date_list)


r_nofollow = re.compile('<a (?![^>]*nofollow)')
s_nofollow = '<a rel="nofollow" '

def nofollow (value):
    return r_nofollow.sub (s_nofollow, value)

register.filter(nofollow)

def gravatar (email, size=50):
	email_hash = hashlib.md5 (email).hexdigest ()
	append_url = urlencode ({u'gravatar_id': email_hash, u'size': size})
	gravitar_url = u"http://www.gravatar.com/avatar.php?%s" % append_url
	return gravitar_url

register.simple_tag (gravatar)

def month_calendar (year=None, month=None):
    # Year and month cannot have default values from datetime as
    # the default values will be static as the program runs
#    print year
#    print month
    if not year or not month:
        current_date = datetime.datetime.now ()
        if not year:
            year = current_date.year
        if not month:
            month = current_date.month
    year, month = int (year), int (month)

    # Gets all dates in a calendar month, including dates not in the month
    base_calendar_month = calendar.Calendar (calendar.SUNDAY).monthdatescalendar (year, month)
    headers = base_calendar_month[0]
    first_day_of_month = datetime.date (year, month, 1)
#    print first_day_of_month
    first_day_of_next_month = datetime.date (year, month, (calendar.monthrange (year, month)[1])) + datetime.timedelta (1)
#    print first_day_of_next_month

    # Find all Post elements published within a given month
    posts = Post.published_objects.filter (pub_date__range=(first_day_of_month, first_day_of_next_month)).order_by ('pub_date')
    post_list = list (posts)
#    print post_list
    previous_month = next_month = None

    try:
        previous_month = Post.published_objects.filter (pub_date__lte=first_day_of_month).order_by ("-pub_date")[0]
    except IndexError, e:
        pass

    try:
        next_month = Post.published_objects.filter (pub_date__gte=first_day_of_next_month).order_by ("pub_date")[0]
    except IndexError, e:
        pass

#    if len (post_list) >= 1:
#        previous_month = post_list[0].get_previous_post ()
#        next_month = post_list[-1].get_next_post ()
#   if previous_month:
#       print previous_month.pub_date
#   if next_month:
#       print next_month.pub_date
	
    # Loop through elements in the base calendar and fill a new calendar list
    # with the days and posts for a month
    calendar_month = []
    for base_week in base_calendar_month:
        week = []
        for day in base_week:
            cal_day = {'day': day, 'item': None}
            if len (post_list) == 0:
                week.append (cal_day)
                continue
            removed_indexes = []
            for i, post in enumerate (post_list):
                if day == post.pub_date.date () and not cal_day['item']:
                    cal_day['item'] = post
                    removed_indexes.insert (0, i)
                elif day == post.pub_date.date ():
                    removed_indexes.insert (0, i)

            for index in removed_indexes:
                del post_list[index]

            week.append (cal_day)
        calendar_month.append (week)
    #print calendar_month

    return {'calendar': calendar_month, 'headers': headers, 'first_day': first_day_of_month, 'previous_month': previous_month, 'next_month': next_month}

register.inclusion_tag ("blog/templatetags/calendar.html")(month_calendar)


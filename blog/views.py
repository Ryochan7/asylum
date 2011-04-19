from django.views.generic.date_based import object_detail
from django.views.generic.date_based import archive_month, archive_day
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
import datetime, calendar
from time import strptime
from tagging.models import Tag, TaggedItem
from blog.models import Post
from blog.forms import SearchForm

# Create your views here.

entries_detail = {
    "queryset": Post.published_objects.select_related ().all (),
    "template_name": "blog/post_detail.html",
    "template_object_name": "post",
    "slug_field": "slug",
    "date_field": "pub_date",
    "month_format": "%m",
    "extra_context": {"search_form": SearchForm ()}
}

entries_month = {
    "queryset": Post.published_objects.select_related ().all (),
    "month_format": "%m",
    "template_name": "blog/month_list.html",
    "template_object_name": "post",
    "date_field": "pub_date",
    "allow_empty": True,
    "extra_context": {"search_form": SearchForm ()}
}

entries_day = entries_month.copy ()
entries_day.update ({"template_name": "blog/day_list.html"})


def home_view (request):
    if request.GET.get ("page"):
        return HttpResponseRedirect ("%s?page=%s" % (reverse ("blog_home_view"), request.GET.get ("page")))

    return blog_home_view (request, "base.html")


def blog_home_view (request, template="blog/base.html"):
    context = {
        "post_list": Post.published_objects.select_related ().all (),
        "search_form": SearchForm ()
    }
    return direct_to_template (request, template, context)


def search_view (request):
    if request.GET.get ('search'):
        form = SearchForm (request.GET)
        if form.is_valid ():
            # Get sphinx results only. Will not perform a database query
            if getattr (Post, "search", None):
                results = Post.search.query (form.cleaned_data['search']).filter (published=True)._get_sphinx_results ()
                pks = [result['id'] for result in results.get ('matches')]
                post_list = Post.published_objects.filter (pk__in=pks).select_related ()
                #print pks

            else:
                # Use slow searching if Sphinx is not available
                post_list = Post.published_objects.filter (title__icontains=form.cleaned_data["search"]).select_related () | Post.published_objects.filter (body__icontains=form.cleaned_data["search"]).select_related ()
                
            context = {
                "post_list": post_list,
                "search_form": form,
                "search_term": request.GET.get ('search')
            }
            return direct_to_template (request, "blog/search_results.html", context)
    else:
        raise Http404


def post_detail_view (request, year, month, day, slug):
    return object_detail (request, year=year, month=month, day=day, slug=slug, **entries_detail)


def month_view (request, year, month):
    try:
        d = datetime.date(*strptime(year + month, '%Y%m')[:3])
    except ValueError:
        raise Http404
    year, month = int (year), int (month)


    first_day = datetime.date (year, month, 1)
    last_day = datetime.date (year, month, (calendar.monthrange (year, month)[1])) + datetime.timedelta (1)
    r = (first_day, last_day)

    post_list = Post.published_objects.filter (pub_date__range=r).select_related ()

    previous_month = next_month = None
    try:
        previous_month = Post.published_objects.filter (pub_date__lte=first_day).order_by ("-pub_date")[0]
    except IndexError, e:
        pass

    try:
        next_month = Post.published_objects.filter (pub_date__gte=last_day).order_by ("pub_date")[0]
    except IndexError, e:
        pass

    context = {
        "post_list": post_list,
        "search_form": SearchForm (),
        "month": d,
        "next_month": next_month,
        "previous_month": previous_month,
    }
    return direct_to_template (request, "blog/month_list.html", context)
#    return archive_month (request, year=year, month=month, **entries_month)


def day_view (request, year, month, day):
    try:
        d = datetime.date(*strptime(year + month + day, '%Y%m%d')[:3])
    except ValueError:
        raise Http404

    r = (datetime.datetime.combine(d, datetime.time.min), datetime.datetime.combine(d, datetime.time.max))
    post_list = Post.published_objects.filter (pub_date__range=r).select_related ()

    next_day = previous_day = None
    try:
        next_day = Post.published_objects.filter (pub_date__gte=d+datetime.timedelta (1)).order_by ("pub_date")[0]
    except IndexError, e:
        pass

    try:
        previous_day = Post.published_objects.filter (pub_date__lt=d)[0]
    except IndexError, e:
        pass

    context = {
        "post_list": post_list,
        "search_form": SearchForm (),
        "day": d,
        "next_day": next_day,
        "previous_day": previous_day,
    }
    return direct_to_template (request, "blog/day_list.html", context)
#   return archive_day (request, year=year, month=month, day=day, **entries_day)

def tag_view (request, tag):
    current_tag = get_object_or_404 (Tag, name=tag)
    context = {
        "post_list": TaggedItem.objects.get_by_model (Post, current_tag).select_related ().filter (published=True),
        "tag": current_tag,
        "tag_feed": "tag/%s" % current_tag.name,
        "search_form": SearchForm ()
    }
    return direct_to_template (request, "blog/tagged_items.html", context)


def post_preview_view (request, year, month, day, slug):
    if request.user.is_authenticated ():
        try:
            d = datetime.date(*strptime(year + month + day, '%Y%m%d')[:3])
        except ValueError:
            raise Http404

        r = (datetime.datetime.combine(d, datetime.time.min), datetime.datetime.combine(d, datetime.time.max))
        post = get_object_or_404 (Post, pub_date__range=r, slug__exact=slug)
        if request.user != post.author:
            raise Http404
        context = {
            "post": post,
            "search_form": SearchForm (),
        }
        return direct_to_template (request, "blog/post_preview.html", context)
    raise Http404



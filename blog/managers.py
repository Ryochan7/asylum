from django.db import models

class PublishedPostManager (models.Manager):
    def get_query_set (self):
        queryset = super (PublishedPostManager, self).get_query_set ()
        return queryset.filter (published=True)



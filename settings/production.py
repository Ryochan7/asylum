from settings.common import *
# Remove database settings imported from common.py. Will cause Django
# to produce an error if DATABASES is not configured in secrets.py
DATABASES = {
}
from settings.secerts import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "http://www.ryochan7.com/media/"
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/admin/"

SPHINX_API_VERSION = 0x113
SPHINX_SERVER = 'localhost'
SPHINX_PORT = 7671

PINGBACK_LINKS = True
DIRECTORY_URLS = (
    'http://ping.blogs.yandex.ru/RPC2',
)

DISQUS_DEVELOPER = 0
PAGINATE_BY = 10
ANALYTICS = True
CONTACT_SEND_ADMIN_MAIL = True



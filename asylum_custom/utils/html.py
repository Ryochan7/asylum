def thumbnails(html):
    """
    Given a HTML string, converts paths in img tags to thumbnail
    paths, using Mezzanine's ``thumbnail`` template tag. Used as
    one of the default values in the ``RICHTEXT_FILTERS`` setting.
    """
    from django.conf import settings
    from html5lib.treebuilders import getTreeBuilder
    from html5lib.html5parser import HTMLParser
    #from mezzanine.core.templatetags.mezzanine_tags import thumbnail
    from asylum_custom.templatetags.asylum_tags import thumbnail

    dom = HTMLParser(tree=getTreeBuilder("dom")).parse(html)
    for img in dom.getElementsByTagName("img"):
        src = img.getAttribute("src")
        width = img.getAttribute("width")
        height = img.getAttribute("height")
        if src and width and height:
            src = settings.MEDIA_URL + thumbnail(src, width, height)
            img.setAttribute("src", src)
    nodes = dom.getElementsByTagName("body")[0].childNodes
    return "".join([node.toxml() for node in nodes])


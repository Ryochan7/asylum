import markdown
from markdown import etree

class YouTubeEmbedPattern (markdown.inlinepatterns.Pattern):
    def handleMatch (self, m):
        el = etree.Element ("object", {"type": "application/x-shockwave-flash", "width": "425", "height": "344", "data": "http://www.youtube.com/v/%s" % m.group (2)})
        sub = etree.Element ("param", {"name": "movie", "value": "http://www.youtube.com/v/%s" % m.group (2)})
        el.append (sub)
        sub = etree.Element ("param", {"name": "allowFullScreen", "value": "true"})
        el.append (sub)
        sub = etree.Element ("param", {"name": "allowscriptaccess", "value": "always"})
        el.append (sub)
        sub = etree.Element ("param", {"name": "wmode", "value": "transparent"})
        el.append (sub)

        return el


class YouTubeEmbedExtension (markdown.Extension):
    def extendMarkdown (self, md, md_globals=None):
        new_pattern = YouTubeEmbedPattern (r'==youtube\(http://(?:www\.)?youtube\.com/watch\?v=(\S+)\)==')
        md.inlinePatterns.add ("youtube_embed", new_pattern, "_end")


def makeExtension (configs=None):
    return YouTubeEmbedExtension (configs=configs)


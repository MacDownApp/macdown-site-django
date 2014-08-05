from django.core.urlresolvers import reverse
from django.utils import feedgenerator
from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed
from .posts import get_post_list


MACDOWN_DESCRIPTION = _(
    '<p>MacDown is an open source Markdown editor for OS X, released under '
    'the MIT License. It is heavily influenced by '
    '<a href="https://twitter.com/chenluois">Chen Luo</a>’s '
    '<a href="http://mouapp.com">Mou</a>.</p>'
)


class PostsFeed(Feed):
    """Common parent class for RSS and Atom feeds
    """

    title = _('The MacDown Blog')
    description = MACDOWN_DESCRIPTION

    def link(self):
        return reverse('blog:list')

    def items(self):
        return get_post_list()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.rendered_content

    def item_link(self, item):
        return item.get_absolute_url()


class PostsRss201rev2Reed(PostsFeed):
    feed_type = feedgenerator.Rss201rev2Feed


class PostsAtom1Feed(PostsFeed):
    feed_type = feedgenerator.Atom1Feed


rss201rev2 = PostsRss201rev2Reed()
atom1 = PostsAtom1Feed()

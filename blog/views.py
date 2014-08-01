import os
import mistune
from django.http import Http404, HttpResponsePermanentRedirect
from django.views.generic import TemplateView
from .posts import Post, PostDoesNotExist, get_post_filelist, get_post_filename
from .utils import Renderer, resolve_prism_languages


# id => post instance
_post_cache = {}


class PostListView(TemplateView):

    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        posts = []
        for filename in reversed(get_post_filelist()):
            try:
                base, _ = os.path.splitext(filename)
                post_id = int(Post.FILENAME_PATTERN.match(base).group(1))
                post = _post_cache[post_id]
            except (AttributeError, KeyError):
                try:
                    post = Post(filename)
                except PostDoesNotExist:
                    continue
                _post_cache[post.id] = post
            if post.title:
                posts.append(post)
        data = super().get_context_data()
        data.update({'posts': posts})
        return data


class PostDetailView(TemplateView):

    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        post_id = int(kwargs['id'])
        post_slug = kwargs.get('slug')
        try:
            post = _post_cache[post_id]
        except KeyError:
            try:
                post = Post(get_post_filename(id=post_id))
            except PostDoesNotExist:
                raise Http404
            _post_cache[post_id] = post
        if post.slug != post_slug:
            canonical_url = post.get_absolute_url()
            return HttpResponsePermanentRedirect(redirect_to=canonical_url)
        self.post = post
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            page_meta, content = self.post.file_content
            assert page_meta is not None
        except (AssertionError, PostDoesNotExist):
            raise Http404

        renderer = Renderer()
        data = super().get_context_data()
        data.update({
            'page': page_meta,
            'content': mistune.markdown(content, renderer=renderer),
            'languages': resolve_prism_languages(renderer.languages),
        })
        return data


post_list = PostListView.as_view()
post_detail = PostDetailView.as_view()

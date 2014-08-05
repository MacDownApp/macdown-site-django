from django.http import Http404, HttpResponsePermanentRedirect
from django.views.generic import TemplateView
from .posts import PostDoesNotExist, get_post_list, get_post
from .utils import resolve_prism_languages


class PostListView(TemplateView):

    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        posts = get_post_list()
        data = super().get_context_data()
        data.update({'posts': posts})
        return data


class PostDetailView(TemplateView):

    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        post_id = int(kwargs['id'])
        post_slug = kwargs.get('slug')
        try:
            post = get_post(post_id)
        except PostDoesNotExist:
            raise Http404
        if post.slug != post_slug or kwargs['id'] != str(post_id):
            canonical_url = post.get_absolute_url()
            return HttpResponsePermanentRedirect(redirect_to=canonical_url)
        self.post = post
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            page_meta = self.post.meta
            content = self.post.rendered_content
            renderer = self.post.renderer
            assert page_meta is not None
            assert renderer is not None
        except (AssertionError, PostDoesNotExist):
            raise Http404
        data = super().get_context_data()
        data.update({
            'post': self.post,
            'page': page_meta,
            'content': content,
            'languages': resolve_prism_languages(renderer.languages),
        })
        return data


post_list = PostListView.as_view()
post_detail = PostDetailView.as_view()

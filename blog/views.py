import mistune
from django.http import Http404, HttpResponsePermanentRedirect
from django.views.generic import TemplateView
from .posts import Post, PostDoesNotExist, get_post_filelist, get_post_filename
from .utils import Renderer, resolve_prism_languages


class PostListView(TemplateView):

    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        posts = []
        for filename in reversed(get_post_filelist()):
            try:
                post = Post(filename)
            except PostDoesNotExist:
                continue
            if post.title:
                posts.append(post)
        data = super().get_context_data()
        data.update({'posts': posts})
        return data


class PostDetailView(TemplateView):

    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        post_slug = kwargs.get('slug')
        try:
            post = Post(get_post_filename(id=kwargs['id']))
        except PostDoesNotExist:
            raise Http404
        if post.slug != post_slug:
            canonical_url = post.get_absolute_url()
            return HttpResponsePermanentRedirect(redirect_to=canonical_url)
        self.post = post
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            post_data, content = self.post.file_content
            assert post_data is not None
        except (AssertionError, PostDoesNotExist):
            raise Http404

        renderer = Renderer()
        post_data['content'] = mistune.markdown(content, renderer=renderer)
        data = super().get_context_data()
        data.update({
            'post': post_data,
            'languages': resolve_prism_languages(renderer.languages),
        })
        return data


post_list = PostListView.as_view()
post_detail = PostDetailView.as_view()

import mistune
from django.http.response import HttpResponsePermanentRedirect
from django.views.generic import TemplateView
from .posts import Post, get_post_filename


class PostDetailView(TemplateView):

    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        post_slug = kwargs.get('slug')
        post = Post(get_post_filename(id=kwargs['id']))
        if post.slug != post_slug:
            canonical_url = post.get_absolute_url()
            return HttpResponsePermanentRedirect(redirect_to=canonical_url)
        self.post = post
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        post_data, content = self.post.file_content
        post_data['content'] = mistune.markdown(content)
        data = super().get_context_data()
        data['post'] = post_data
        return data


post = PostDetailView.as_view()

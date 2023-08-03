from blog.models import Post
from django.shortcuts import redirect


class PostMixin:
    model = Post


class PostDispatchMixin:

    def dispatch(self, request, *args, **kwargs):
        self.post_id = kwargs['post_id']
        instance = self.get_object()
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

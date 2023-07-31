from datetime import datetime as dt

from django.shortcuts import get_object_or_404, render

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.all().filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=dt.now()
    ).order_by('id')[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=dt.now()
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True
    )
    post_list = category.posts.filter(
        pub_date__lte=dt.now(),
        category_id=category,
        is_published=True
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from django.views.generic import (
    CreateView, DetailView, DeleteView, ListView, UpdateView
)

from .forms import PostForm, CommentForm, UserForm
from blog.models import Post, Category, Comment
from users.models import MyUser
from .mixins import PostMixin, PostDispatchMixin

PAGINATOR = 10


class IndexListView(PostMixin, LoginRequiredMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = PAGINATOR

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            'author',).order_by('-pub_date').filter(
            pub_date__lte=timezone.now(), is_published=True,
            category__is_published=True).annotate(
                comment_count=Count('comments'))
        return queryset


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'blog/detail.html'
    paginate_by = PAGINATOR
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        if get_object_or_404(
            Post.objects.filter(pk=self.kwargs['post_id']
                                )).author == self.request.user:
            return Post.objects.filter(pk=self.kwargs['post_id'])
        return Post.objects.filter(pub_date__lte=timezone.now(),
                                   is_published=True,
                                   category__is_published=True)

    def get_context_data(self, **kwargs):
        context = dict(**super().get_context_data(**kwargs),
                       form=CommentForm(),
                       comments=self.object.comments.select_related('author'))
        return context


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, post_id=post_id, id=comment_id)
    if comment.author != request.user:
        return redirect('login')
    form = CommentForm(request.POST or None, instance=comment)
    context = {
        'form': form,
        'comment': comment}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, post_id=post_id, id=comment_id)
    if comment.author != request.user:
        return redirect('login')
    context = {
        'comment': comment
    }
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


class CommentCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])

    def dispatch(self, request, *args, **kwargs):
        self._post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self._post
        return super().form_valid(form)


class PostCreateViews(PostMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            url = reverse('blog:profile',
                          args=(self.request.user.get_username(),))
        else:
            url = reverse('login')
        return url


class PostUpdateView(PostMixin, LoginRequiredMixin, PostDispatchMixin,
                     UpdateView):
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[str(self.post_id)])


class PostDeleteView(PostMixin, LoginRequiredMixin, PostDispatchMixin,
                     DeleteView):
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class ProfileListView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = PAGINATOR
    fields = '__all__'

    def get_queryset(self):
        profile = get_object_or_404(
            MyUser,
            username=self.kwargs['username']
        )
        return Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date').filter(author=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            MyUser,
            username=self.kwargs['username']
        )
        return context


class ProfiletUpdateView(UpdateView):
    model = MyUser
    form_class = UserForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        obj = get_object_or_404(MyUser, username=self.request.user)
        return obj

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user])


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = PAGINATOR

    def get_queryset(self):
        category = get_object_or_404(Category,
                                     slug=self.kwargs['slug'],
                                     is_published=True).posts.select_related(
            'author',).order_by('-pub_date').filter(
            pub_date__lte=timezone.now(), is_published=True).annotate(
            comment_count=Count('comments'))
        return category

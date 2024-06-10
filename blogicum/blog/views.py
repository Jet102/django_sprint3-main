from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category
from django.utils.timezone import now


def index(request):

    post_list = get_posts(Post.objects).order_by('-pub_date')[:5]

    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, category_slug):

    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)

    post_list = category.posts.filter(
        pub_date__lte=now(),
        is_published=True)

    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):

    post = get_object_or_404(get_posts(Post.objects), id=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def get_posts(post_objects):
    return post_objects.select_related(
        'location', 'author', 'category'
    ).filter(pub_date__lte=now(),
             is_published=True, category__is_published=True)

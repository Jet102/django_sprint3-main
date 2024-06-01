from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category
from django.utils.timezone import now


def index(request):

    post_list = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(pub_date__lte=now(),
             is_published=True,
             category__is_published=True
             ).order_by('-pub_date')[:5]

    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, category_slug):

    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)

    post_list = Post.objects.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
        category=category)

    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)


def post_detail(request, id):

    post = get_object_or_404(
        Post.objects.select_related(
            'location',
            'author',
            'category',
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=now()
        ),
        id=id)

    return render(request, 'blog/detail.html', {'post': post})

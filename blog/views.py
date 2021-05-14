from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    """
    This takes the request object as its only parameter. This parameter is required by all the views.
    in this view you retrieve all the posts with the published status using the published manager.
    Finally the render() shortcut rendered the posts with the given template. This function takes the
    request object, the template path, and the context variables to render the given template.
    """
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    """
    This view takes teh year, month, day and post arguments to retrieve a published post with
    the given slug and date.  Note that when we created the Post model we added 'unique_for_date'
    parameter to the slug field.  This ensures there will only be one post with a slug for a given
    date, and thus, you can retrieve single posts using the date and slug.
    We use 'get_object_or_404()' shortcut to retrieve the desired post. Then we render as before.
    """
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {"post": post})

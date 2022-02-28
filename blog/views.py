from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import CreateBlogPostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def new_blog_post(request):
    if request.method == 'POST':
        form = CreateBlogPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data['title']
            content = data['content']
            photo = data['photo']

            blog_post_object = BlogPost(title=title,
                                        content=content,
                                        photo=photo,
                                        written_by=request.user)

            blog_post_object.save()

            return redirect('home')
    else:
        form = CreateBlogPostForm()
    return render(request, 'blog/new_blog_post.html', {'form': form})

def view_blog_post(request, pk):
    blog_post = BlogPost.objects.get(pk=pk)
    return render(request, 'blog/view_blog_post.html', {'blog_post': blog_post})

def blog_post_gallery(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog/blog_gallery.html', {'posts': blog_posts})
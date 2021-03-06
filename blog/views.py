from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.models import Friend
from django.contrib import messages

# Create your views here.
def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html',context)

def follow_view(request,username,follow):
    if request.user.is_anonymous:
        messages.add_message(request, messages.INFO,
                             'You need to log in to follow ' + username + ' !')
        return redirect('login')
    blog_viewer = request.user
    blog_author=User.objects.get(username=username)
    # save users to force send signal to create Friend model
    blog_viewer.save()
    blog_author.save()
    blog_viewer_f = Friend.objects.get(user=blog_viewer)
    blog_author_f = Friend.objects.get(user=blog_author)
    print(blog_viewer)
    print(blog_author)
    print(follow)
    if follow == 'Following' or follow == 'Friend':
        blog_viewer_f.following.remove(blog_author)
        blog_author_f.follower.remove(blog_viewer)
    else:
        blog_viewer_f.following.add(blog_author)
        blog_author_f.follower.add(blog_viewer)
    return redirect('user-posts',username)

def like_view(request,cururl,pk):
    if request.user.is_anonymous:
        messages.add_message(request, messages.INFO,
                             'You need to log in to like this post!')
        return redirect('login')
    post = get_object_or_404(Post,id=pk)
    page = request.POST.get('pages')
    page_str = "?page=" + str(page)
    pk_str = '#' + str(pk)
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.save()
        else:
            post.likes.add(request.user)
            post.save()
    if cururl == 'FromUserPost':
        return HttpResponseRedirect(reverse('user-posts',kwargs={'username':post.author.username})+page_str+pk_str)
    elif cururl == 'FromDetail':
        return HttpResponseRedirect(reverse('post-detail',kwargs={'pk':pk})+pk_str)
    else:
        return HttpResponseRedirect(reverse('blog-home')+page_str+pk_str)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # default <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # default <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if self.request.user.is_authenticated:
            self.request.user.save() # save user to force send signal to create Friend model
            myfriend = Friend.objects.get(user=self.request.user)
            to_follow = Friend.is_friends(myfriend,user)
        else:
            to_follow = 'UserNotLogIn'
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context.update({'users': user })
        context.update({'follow':to_follow})
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        # return super().get_queryset()

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','image']

    def form_valid(self,form,*args,**kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form,*args,**kwargs)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content','image']

    def form_valid(self,form,*args,**kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form,*args,**kwargs)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html')
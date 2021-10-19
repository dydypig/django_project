from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html',context)

def like_view(request,cururl,pk):
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
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context.update({'users': user })
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
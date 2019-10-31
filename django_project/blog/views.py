from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

posts = [

    {
        'author': 'José Eduardo',
        'title': 'Blog Post',
        'content': 'First Post',
        'date_posted': 'October 19, 2019'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post',
        'content': 'Seconde Post',
        'date_posted': 'October 20, 2019'
    }

]

# function view
# def home(request):
#     context = {
#         # 'posts': posts
#         'posts':Post.objects.all()
#     }
#     return render(request, "blog/home.html", context)


def about(request):
    return render(request, "blog/about.html", {'title': 'About'})

# list view 
class PostListView(ListView):
    model = Post
    # app/model_viewtype.html
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
class UserPostListView(ListView):
    model = Post
    # app/model_viewtype.html
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    

# with LoginRequiredMixin if user tries to access /post/new and is not logged in
 # he'll be redirected to login pagin
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # sets the author
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # sets the author
        form.instance.author = self.request.user
        return super().form_valid(form)

# prevent users to update someone elses post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
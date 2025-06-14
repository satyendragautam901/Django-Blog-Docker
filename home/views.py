from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

# <------ function based views ----->

def test(request):
    if request.method =="POST":
        return HttpResponse("This is Post method")
    elif request.method =="GET": 
        return HttpResponse("This is get method call")
        
def Register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User(first_name = first_name,
                    last_name = last_name,
                    email = email,
                    username = username)
        
        user.set_password(password)
        try:

            user.save()
            print("user created successfully")

        except:
            print("error during registering user ")



    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            print("User logged in successfully")
            return redirect('blogs')  # Redirect to home or dashboard
        else:
            return HttpResponse("Invalid username or password")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    print("logout successfully")
    return redirect('/')


def all_blogs(request):
    if not request.user.is_authenticated:
        return redirect('login')  # or show empty list or error

    blogs = Blog.objects.filter(author=request.user)  # only current user's blogs
    context = {'blogs': blogs}
    return render(request, 'blogs.html', context)


@login_required
def details_page(request, id):
    try:
        blog = Blog.objects.get(id = id)
    except Blog.DoesNotExist:
            return HttpResponse(f"No blog post found with id: {id}")
    
    return render(request, 'details.html', {'blog':blog})


@login_required
def create_blog(request):
    if request.method == "POST":
        print("this is rewust",request.method)
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        print("author during creating ",author)

        print("this is title",title, content, author)

        try:
            # Create a new Blog
            Blog.objects.create(title=title, content=content, author=author)

            # <--- reverse is used here in FBVs ----->

            return redirect(reverse('blogs')) 
        except Exception as e:
            return HttpResponse(f"Error during creating blog: {e}")

    return render(request, 'create.html')

@login_required
def update_blog(request, id):
    post = Blog.objects.get(id = id)
    if request.method =="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')

        post.title = title
        post.content = content
        post.author = author

        try:
            post.save()
            return redirect(reverse('blogs'))
        except:
            return HttpResponse("Error during updating post")
        
    return render(request, 'update.html', {'post':post})

@login_required
def delete_blog(request, id):
    try:
        blog = Blog.objects.get(id = id)
    except Blog.DoesNotExist:
        return HttpResponse(f"No blog wi this {id}")

    try:
        blog.delete()
        return redirect(reverse('blogs'))

    except:
        return HttpResponse(f"Error during deleting blog")


def about(request):
    return render(request, 'about.html')


# <------ classs based views ----->

class SeeBlogs(View):
    def get(self, request):
        blogs = Blog.objects.all()
        print("This is class based view")
        context = {'blogs':blogs}
        return render(request, 'blogs.html', context)

    

class DetailsBlog(View):
    def get(self, request, id):
        try:
            blog = Blog.objects.get(id = id)

        except Blog.DoesNotExist:
            return HttpResponse(f"No blog with this {id}")
        
        return render(request, 'details.html', {'blog':blog})

class CreateBlog(View):
    def get(self, request):
        return render(request, 'create.html')
    
    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        try:
            # Create a new Blog
            Blog.objects.create(title=title, content=content, author=author)
            return redirect(reverse('blogs'))  
        except Exception as e:
            return HttpResponse(f"Error during creating blog: {e}")
        
    
class UpdateBlog(View):
    def get(self, request, id):
        try:
            post = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return HttpResponse(f"No blog post found with id: {id}")
        
        return render(request, 'update.html', {'post':post})
    
    def post(self, request, id):
        try:
            post = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return HttpResponse(f"No blog post found with id: {id}")
        
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.author = request.POST.get('author')

        try:
            post.save()
            return redirect(reverse('blogs'))
        except Exception as e:
            return HttpResponse(f"Error during updating: {e}")
        

class DeleteBlog(View):
    def get(self, request, id):
        try:
            post = Blog.objects.get(id = id)

        except Blog.DoesNotExist:
            return HttpResponse(f"No blog with this {id}")
        
        return render(request, 'delete_confirm.html', {'post':post})
        
    def post(self, request, id):
        try:
            post = Blog.objects.get(id = id)

        except Blog.DoesNotExist:
            return HttpResponse(f"No blog with this {id}")
        
        try:
            post.delete()
            return redirect(reverse('cbv_seeblogs'))
        except Exception as e:
            return HttpResponse(f"Error during deleting blog{e}")
        
# <--- generic view ----->

class SeeblogsGeneric(ListView):
    model = Blog
    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 3

class CreateBlogGeneric(CreateView):
    model = Blog
    template_name = 'create.html'
    fields = ['title', 'content', 'author']
    success_url = reverse_lazy('blogs')

class UpdateBlogGeneric(UpdateView):
    model = Blog
    template_name = 'update.html'
    fields = ['title', 'content', 'author']
    context_object_name = "post"
    success_url = reverse_lazy('gen_seeblogs')

class DetailiBlogGeneric(DetailView):
    model = Blog
    template_name = 'details.html'

    # context object name is make populated data . in details.html blog.title is accessible only context name
    context_object_name = "blog"

class DeleteBlogGeneric(DeleteView):
    model = Blog
    template_name = 'delete_confirm.html'
    context_object_name = 'post'
    success_url = reverse_lazy('gen_seeblogs')


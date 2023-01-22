from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView,UpdateView

from socialweb.forms import UserRegistrationForm,LoginForm,PostForm,ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from api.models import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages


def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"you must login first")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

decs=[signin_required,never_cache]

class RegistrationView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")


class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                messages.error(request,"invalid credentials")
                print("invalid")
                return redirect("signin")

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("home")
    context_object_name="posts"
    queryset=Posts.objects.all()

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user=self.request.user
            messages.success(self.request,"post created")
            return super().form_valid(form)
        else:
            return render(self.request,"index.html",{"form":form})
        

    def get_queryset(self):
        return Posts.objects.exclude(user=self.request.user).order_by("-created_date")

@method_decorator(signin_required,name="dispatch")
class ProfileView(CreateView,ListView):
    template_name="myprofile.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("home")
    context_object_name="posts"
    queryset=Posts.objects.all()

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user).order_by("-created_date")
   

decs
def add_comment(request, *args, **kwargs):
        id = kwargs.get('id')
        cmt = request.POST.get('comment')
        qs = Posts.objects.get(id=id)
        qs.comments_set.create(user=request.user, comment=cmt)
        messages.success(request, "Comment added succesfully")
        return redirect("home")

def like_post(request, *args, **kwargs):
        id = kwargs.get('id')
        ps = Posts.objects.get(id=id)
        if ps.like.contains(request.user):
            ps.like.remove(request.user)
        else:
            ps.like.add(request.user)
        return redirect("home")

def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("signin")

method_decorator(decs,name="dispatch")
class EditProfileView(UpdateView):
    template_name="editprofile.html"
    form_class=ProfileForm
    model=Userprofile
    pk_url_kwarg="id"
    success_url=reverse_lazy("myprofile")



@method_decorator(decs,name="dispatch")
class AddProfile(CreateView):
    template_name="userprofile.html"
    form_class=ProfileForm
    success_url=reverse_lazy("index")
    def post(self,request,*args,**kwargs):
        form=ProfileForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect("index")
        else:
            return render(request,"userprofile.html",{"form":form})



method_decorator(decs,name="dispatch")
class ListPeopleView(ListView):
    template_name="peoples.html"
    model = User
    context_object_name = 'people'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        context["posts"] = Posts.objects.all().order_by('-created_date')
        return context
    

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)
 

def add_follower(request, *args, **kwargs):
    id = kwargs.get('id')
    usr = User.objects.get(id=id)
    if not Friends.objects.filter(user=usr, follower=request.user):
        Friends.objects.create(user=usr, follower=request.user)
    else:
        Friends.objects.get(user=usr, follower=request.user).delete()
    return redirect("people")

decs
def comment_delete(request,*args,**kw):
    id=kw.get("id")
    Comments.objects.get(id=id).delete()
    return redirect("home")

    













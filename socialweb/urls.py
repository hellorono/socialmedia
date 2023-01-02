from django.urls import path
# from socialweb import views
from .views import *


urlpatterns = [
    path("register",RegistrationView.as_view(),name="signup"),
    path("login",LoginView.as_view(),name="signin"),
    path("index",IndexView.as_view(),name="home"),
    path("logout",sign_out_view,name="sign-out"),
    path("post/<int:id>/comment/add", add_comment, name="add_comment"),
    path("post/<int:id>/like/add", like_post, name="like-post"),
    
]

# path("posts/<int:id>",PostDetailView.as_view(),name="post-detail"),
#     path("posts/<int:id>/remove",post_delete_view,name="post-delete"),
#     path("logout",sign_out_view,name="sign-out")


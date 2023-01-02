from django.shortcuts import render

# Create your views here.
from api.serializers import UserSerializer,PostsSerializer,CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Posts,Comments
from rest_framework import authentication,permissions
from rest_framework.decorators import action

class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class PostsView(ModelViewSet):
    serializer_class=PostsSerializer
    queryset=Posts.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["GET"],detail=False)
    def my_posts(self,request,*args,**kw):
        qs=request.user.posts_set.all()
        serializer=PostsSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        usr=request.user
        serializer=CommentSerializer(data=request.data,context={"post":pos,"user":usr})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["get"],detail=True)
    def list_comments(self,request,*args,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        qs=pos.comments.set_all()
        serializer=CommentSerializer(qs,many=True)
        return Response(data=serializer.data)

# class CommentsView(ModelViewSet):
#     serializer_class=PostsSerializer
#     queryset=Posts.objects.all()
#     authentication_classes=[authentication.BasicAuthentication]
#     permission_classes=[permissions.IsAuthenticated]

    @action(methods=["get"],detail=True)
    def like(self,request,*args,**kw):
        pos=self.get_object()
        usr=request.user
        pos.like.add(usr)
        return Response(data="created")



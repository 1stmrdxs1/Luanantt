from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('post/<str:pk>/', views.post, name="post"),
    path('like/<str:pk>/', views.like, name="like-post"),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),


    path('create-post/', views.createPost, name="create-post"),
    path('update-post<str:pk>/', views.updatePost, name="update-post"),
    path('delete-post<str:pk>/', views.deletePost, name="delete-post"),
    path('delete-comment<str:pk>/', views.deleteComment, name="delete-comment"),

    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('change-password/', views.changePassword, name="change-password"),
]
"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register'),
    path('profile/<int:user_id>/', views.edit_profile, name='edit-profile'),
    path('login/', views.login_user, name='login'),  
    path('create-post/<int:user_id>/', views.create_blog_post, name='create-blog-post'),
    path('blog-posts/<int:user_id>/', views.list_blog_posts, name='list_blog_posts'),
    path('blog-posts/edit/<int:user_id>/<int:post_id>/', views.update_blog_post, name='update_blog_post'),
    path('blog-posts/delete/<int:user_id>/<int:post_id>/', views.delete_blog_post, name='delete_blog_post'),
    path('blog-posts/detail/<int:user_id>/<int:post_id>/', views.detail_blog_post, name='detail_blog_post'), 
    path('blog/<int:user_id>/<int:post_id>/', views.detail_blog_post_view, name='detail_blog_post'),
    path('blog-posts/edit/<int:user_id>/<int:post_id>/', views.edit_blog_post_view, name='edit_blog_post'),
    path('blog-posts/update/<int:user_id>/<int:post_id>/', views.update_blog_post, name='update_blog_post'),  # Ensure this is also defined
    


    path('register1/',views.register_page,name='register_page'),
    path('',views.login_page,name='login_page'),
    path('blog1/',views.blog_page,name='blog1'),
    path('blog_list/',views.blog_list,name='blog_list'),
    path('edit_profile/',views.edit_profile1,name='edit_profile'),
    path('single_post/',views.single_post,name='single_post'),
    path('edit_post/',views.edit_post,name='edit_post'),
    

]



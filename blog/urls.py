from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Blog URLs
    path('blog/blogs/', views.blog_list, name='blog_list'),  # All blogs
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),  # Blog details
    path('blog/create/', views.create_post, name='create_post'),  # Create blog
    path('blog/<int:blog_id>/update/', views.update_post, name='update_post'),  # Update blog
    path('blog/<int:blog_id>/delete/', views.delete_post_confirm, name='delete_post'),  # Delete blog
    path('blog/<int:blog_id>/add_comment/', views.add_comment, name='add_comment'),  # Add comment

    # Author Detail and Blogger List URLs
    path('blogger/<int:author_id>/', views.author_detail, name='author_detail'),  # Author detail
    path('blog/bloggers/', views.blogger_list, name='blogger_list'),  # All bloggers

    # Search URL
    path('search/', views.search_results, name='search_results'),

    # Like and Dislike URLs
    path('like/<int:post_id>/', views.like_post, name='like_post'),  # Like post
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),  # Dislike post

    # User Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Login
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Logout
    path('signup/', views.signup, name='signup'),  # Signup
    path('registration/register/', views.register, name='register'),  # Registration
    
    # Profile URL
    path('profile/', views.profile, name='profile'),  # User profile
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

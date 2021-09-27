from django.urls import path
#from . import views
from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, AddCategoryView, CategoryView, LikeView, add_comments, get_country, author_all_posts, get_bloggers, save_comment, index, add_post

urlpatterns = [
    #path('', views.home, name = "home"),
    path('', HomeView.as_view(), name = "home"),
    # path('', index, name = "home"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name = "article-detail"),
    path('add_post/', add_post, name = "add_post"),
    path('add_category/', AddCategoryView.as_view(), name = "add_category"),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name = "update_post"),
    path('article/<int:pk>/delete', DeletePostView.as_view(), name = "delete_post"),
    path('category/<str:cats>/', CategoryView, name = "category"),
    path('like/<int:pk>', LikeView, name = "like_post"),
    path('article/<int:pk>/comment', add_comments, name = "add_comment"),
    path('save_comment', save_comment, name = "save_comment"),
    #path('category2/<str:bloggers>/', CategoryView2, name = "bloggers"),

    path('get_country', get_country, name="get_country"),
    path('get_bloggers', get_bloggers, name="get_bloggers"),
    path('author_all_posts/<int:pk>', author_all_posts, name="author_all_posts"),

]

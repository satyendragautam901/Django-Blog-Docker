from django.urls import path
from .views import *
urlpatterns = [
    path('', all_blogs, name="blogs"),
    path('aboutPage/', about, name="about"),
    path('create-blog/',create_blog, name = "create_blog"),
    path('update-blog/<int:id>',update_blog, name="update_blog"),
    path('details/<int:id>', details_page, name = "details"),
    path('delete/<int:id>', delete_blog, name = "delete"),

    # login and signup 
    path('register/', Register_view, name = "register"),
    path('login/', login_view, name = "login"),
    path('logout/', logout_view, name = "logout"),

    # class based 

    path('cl/blogs', SeeBlogs.as_view(), name="cbv_seeblogs"),
    path('cl/create-blog/',CreateBlog.as_view(), name = "cbv_create_blog"),
    path('cl/update-blog/<int:id>',UpdateBlog.as_view(), name="cbv_update_blog"),
    path('cl/details/<int:id>',DetailsBlog.as_view(), name="cbv_details_blog"),
    path('cl/delete/<int:id>',DeleteBlog.as_view(), name="cbv_delete_blog"),
    


    # generic class based 

    path('gv/blogs', SeeblogsGeneric.as_view(), name="gen_seeblogs"),
    path('gv/create-blog/', CreateBlogGeneric.as_view(), name="gen_create_blog"),
    path('gv/update-blog/<int:pk>', UpdateBlogGeneric.as_view(), name="gen_update_blog"),
    path('gv/details/<int:pk>', DetailiBlogGeneric.as_view(), name="gen_detail_blog"),
    path('gv/delete/<int:pk>', DeleteBlogGeneric.as_view(), name="gen_delete_blog"),
]

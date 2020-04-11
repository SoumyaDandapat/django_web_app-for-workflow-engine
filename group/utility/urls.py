from django.urls import path, re_path
from .import views

urlpatterns = [
    path('',views.registration  , name='registration'),
    path('form',views.form , name = 'form'),
    path('index' ,views.login_request, name = 'index'),
    path('get_data' ,views.get_data, name = 'get_data'),
    path('post_data' ,views.post_data, name = 'post_data'),
    path('admin' ,views.admin, name = 'admin'),
    path('user_detail' ,views.user_detail , name='user_detail'),
    path('resetAdmin',views.resetAdmin),
    path('generate_new_application',views.generate_new_application),
    path('see_all_requests',views.see_all_requests),
    path('see_form_status',views.see_form_status),
    path('post_login',views.post_login,name = 'post_login'),
    path('logout',views.logout_view,name='logout'),
    path('detailsofformid/<form_id>', views.detailsofformid, name='detailsofformid'),
    path('detailsofformid/sendBackForReview/<form_id>',views.sendBackForReview, name = "sendBackForReview"),
    path('reply/<form_id>' , views.reply , name ="reply"),
    path('detailsofformid/accept/<form_id>',views.accept , name = "accept"),
    path('detailsofformid/reject/<form_id>',views.reject , name = "reject"),
    path('see_records', views.see_records , name = 'see_records'),
    path('fd_to_user/<form_id>', views.fd_to_user, name = "fd_to_user")
]
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  views as auth_views
from django.urls import path
from accounts import views


urlpatterns = [
    path('register/',views.RegisterPage,name="Registerpage"),
    path('login/',views.LoginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),


    path('home/',views.home,name="home"),
    path('userpage/',views.Userpage,name="userpage"),
    path('account-setting/',views.account_settings,name="account_settings"),


    path('products/',views.products,name="products"),
    path('Createcustomer/',views.Createcustomer,name="Createcustomer"),
    path('<int:pk>/',views.CustomerDetailView,name="customerdetails"),
    path('Createproduct/',views.Createproduct,name="Createproduct"),
    path('Createorder/<int:pk>',views.createOrder,name="Createorder"),
    path('delete/<pk>',views.deleteOrder,name="Deleteorder"),
    path('<pk>/update/',views.updateOrder,name="Orderupdate"),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_complete"),
    
]


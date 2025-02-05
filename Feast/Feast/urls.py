from django.urls import path
from django.contrib import admin
from Feastapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('customer/', views.customer, name='customer'),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('customer_signin/', views.customer_signin, name='customer_signin'),
    path('customer_page/', views.customer_page, name='customer_page'),
    path('place_order/', views.place_order, name='place_order'),
    path('delivery/', views.delivery, name='delivery'),
    path('delivery_boy_application/', views.delivery_boy_application, name='delivery_boy_application'),
    path('delivery_boy_login/', views.delivery_boy_login, name='delivery_boy_login'),
    path('delivery_boy_page/', views.delivery_boy_page, name='delivery_boy_page'),
    path('feast_admin_login/', views.feast_admin_login, name='feast_admin_login'),
    path('feast_page/', views.feast_page, name='feast_page'),
    path('accept_delivery_boy/<int:delivery_boy_id>/', views.accept_delivery_boy, name='accept_delivery_boy'),
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('logout/', views.logout, name='logout'),
    path('about_us/', views.about_us, name='about_us'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('my_orders_delivered/', views.my_orders_delivered, name='my_orders_delivered'),
    path('customer_success/', views.customer_success, name='customer_success'),
]
from django.urls import path
from . import views

urlpatterns=[
path('',views.store,name='store'),
path('cart/',views.cart,name='cart'),
path('tailwind/',views.tailwind,name='tailwind'),
path('checkout/',views.checkout,name='checkout'),
path('update_item/',views.updateItem,name='update_item'),
path('item_details/',views.showItemDetails,name='item_details'),
path('process_order/',views.processOrder,name='process_order'),
path('Login/',views.Login,name='login'),
path('Logout/',views.Logout,name='logout'),
# path('authuser/',views.authuser,name='authuser'),

]
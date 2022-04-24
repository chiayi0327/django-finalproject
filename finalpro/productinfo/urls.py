from django.urls import path
from productinfo.views import (
    CustomerList,
    ProductList,
    ShoppingCartList,
    CartItemList,
    OrderList,
    OrderProductList,
    CustomerDetail,
    ProductDetail,
    ShoppingCartDetail,
    CartItemDetail,
    OrderDetail,
    OrderProductDetail,
    CustomerCreate,
    ProductCreate,
    ShoppingCartCreate,
    CartItemCreate,
    OrderCreate,
    OrderProductCreate,
    CustomerUpdate,
    ProductUpdate,
    ShoppingCartUpdate,

)

urlpatterns = [

    path('customer/',
         CustomerList.as_view(),
         name='productinfo_customer_list_urlpattern'),

    path('customer/<int:pk>/',
         CustomerDetail.as_view(),
         name='productinfo_customer_detail_urlpattern'),

    path('customer/create/',
         CustomerCreate.as_view(),
         name='productinfo_customer_create_urlpattern'),

    path('customer/<int:pk>/update/',
         CustomerUpdate.as_view(),
         name='productinfo_customer_update_urlpattern'),

    path('product/',
         ProductList.as_view(),
         name='productinfo_product_list_urlpattern'),

    path('product/<int:pk>/',
         ProductDetail.as_view(),
         name='productinfo_product_detail_urlpattern'),

    path('product/create/',
         ProductCreate.as_view(),
         name='productinfo_product_create_urlpattern'),

    path('product/<int:pk>/update/',
         ProductUpdate.as_view(),
         name='productinfo_product_update_urlpattern'),

    path('shoppingcart/',
         ShoppingCartList.as_view(),
         name='productinfo_shoppingcart_list_urlpattern'),

    path('shoppingcart/<int:pk>/',
         ShoppingCartDetail.as_view(),
         name='productinfo_shoppingcart_detail_urlpattern'),

    path('shoppingcart/create/',
         ShoppingCartCreate.as_view(),
         name='productinfo_shoppingcart_create_urlpattern'),

    path('shoppingcart/<int:pk>/update/',
         ShoppingCartUpdate.as_view(),
         name='productinfo_shoppingcart_update_urlpattern'),

    path('cartitem/',
         CartItemList.as_view(),
         name='productinfo_cartitem_list_urlpattern'),

    path('cartitem/<int:pk>/',
         CartItemDetail.as_view(),
         name='productinfo_cartitem_detail_urlpattern'),

    path('cartitem/create/',
         CartItemCreate.as_view(),
         name='productinfo_cartitem_create_urlpattern'),

    path('order/',
         OrderList.as_view(),
         name='productinfo_order_list_urlpattern'),

    path('order/<int:pk>/',
         OrderDetail.as_view(),
         name='productinfo_order_detail_urlpattern'),

    path('order/create/',
         OrderCreate.as_view(),
         name='productinfo_order_create_urlpattern'),

    path('orderproduct/',
         OrderProductList.as_view(),
         name='productinfo_orderproduct_list_urlpattern'),

    path('orderproduct/<int:pk>/',
         OrderProductDetail.as_view(),
         name='productinfo_orderproduct_detail_urlpattern'),

    path('orderproduct/create/',
         OrderProductCreate.as_view(),
         name='productinfo_orderproduct_create_urlpattern'),
]

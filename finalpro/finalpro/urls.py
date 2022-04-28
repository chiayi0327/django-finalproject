from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [

    path('',
         RedirectView.as_view(
             pattern_name='productinfo_product_list_urlpattern',
             permanent=False
         )),

    path('about/',
         TemplateView.as_view(
             template_name='productinfo/about.html'),
         name='about_urlpattern'
         ),

    path('admin/', admin.site.urls),

    path('', include('productinfo.urls'))

]

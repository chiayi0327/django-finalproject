from django.shortcuts import redirect


def redirect_root_view(request):
	return redirect('productinfo_product_list_urlpattern')
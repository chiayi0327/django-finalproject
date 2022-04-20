from django.shortcuts import render, get_object_or_404
from django.views import View

from productinfo.forms import CustomerForm
from productinfo.models import (
	Customer,
	Product,
	Shopping_Cart,
	Cart_Item,
	Order,
	Order_Product,
)
from productinfo.utils import ObjectCreateMixin


class CustomerList(View):

	def get(self, request):
		return render(
			request,
			'productinfo/customer_list.html',
			{'customer_list': Customer.objects.all()}
		)


class CustomerDetail(View):

	def get(self, request, pk):
		customer = get_object_or_404(
			Customer,
			pk=pk
		)
		shipping_method = customer.sm_id
		payment_method = customer.pm_id
		order_list = customer.orders.all()
		return render(
			request,
			'productinfo/customer_detail.html',
			{'customer': customer,
			 'shipping_method': shipping_method,
			 'payment_method': payment_method,
			 'order_list': order_list}
		)


class CustomerCreate(ObjectCreateMixin, View):
	form_class = CustomerForm
	template_name = 'productinfo/customer_form.html'


class ProductList(View):

	def get(self, request):
		return render(
			request,
			'productinfo/product_list.html',
			{'product_list': Product.objects.all()}
		)


class ProductDetail(View):

	def get(self, request, pk):
		product = get_object_or_404(
			Product,
			pk=pk
		)
		category = product.category_id
		return render(
			request,
			'productinfo/product_detail.html',
			{'product': product, 'category': category}
		)


class ShoppingCartList(View):

	def get(self, request):
		return render(
			request,
			'productinfo/shoppingcart_list.html',
			{'shoppingcart_list': Shopping_Cart.objects.all()}
		)


class ShoppingCartDetail(View):

	def get(self, request, pk):
		shoppingcart = get_object_or_404(
			Shopping_Cart,
			pk=pk
		)
		customer_id = shoppingcart.customer_id
		shipping_method = shoppingcart.sm_id
		payment_method = shoppingcart.pm_id
		sc_list = shoppingcart.cart_items.all()
		return render(
			request,
			'productinfo/shoppingcart_detail.html',
			{'shoppingcart': shoppingcart,
			 'customer_id': customer_id,
			 'shipping_method': shipping_method,
			 'payment_method': payment_method,
			 'sc_list': sc_list }
		)


class CartItemList(View):

	def get(self, request):
		return render(
			request,
			'productinfo/cartitem_list.html',
			{'cartitem_list': Cart_Item.objects.all()}
		)


class CartItemDetail(View):

	def get(self, request, pk):
		cartitem = get_object_or_404(
			Cart_Item,
			pk=pk
		)
		cart_id = cartitem.cart_id
		product_id = cartitem.product_id
		return render(
			request,
			'productinfo/cartitem_detail.html',
			{'cartitem': cartitem, 'cart_id': cart_id, 'product_id': product_id}
		)


class OrderList(View):

	def get(self, request):
		return render(
			request,
			'productinfo/order_list.html',
			{'order_list': Order.objects.all()}
		)


class OrderDetail(View):

	def get(self, request, pk):
		order = get_object_or_404(
			Order,
			pk=pk
		)
		customer_id = order.customer_id
		shipping_method = order.sm_id
		payment_method = order.pm_id
		product_list = order.order_products.all()
		return render(
			request,
			'productinfo/order_detail.html',
			{'order': order,
			 'customer_id': customer_id ,
			 'shipping_method': shipping_method,
			 'payment_method': payment_method,
			 'product_list':product_list }
		)


class OrderProductList(View):

	def get(self, request):
		return render(
			request,
			'productinfo/orderproduct_list.html',
			{'orderproduct_list': Order_Product.objects.all()}
		)


class OrderProductDetail(View):

	def get(self, request, pk):
		orderproduct = get_object_or_404(
			Order_Product,
			pk=pk
		)
		order_id = orderproduct.order_id
		product_id = orderproduct.product_id
		return render(
			request,
			'productinfo/orderproduct_detail.html',
			{'orderproduct': orderproduct,
			 'order_id': order_id,
			 'product_id': product_id}
		)
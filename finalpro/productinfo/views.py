from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from productinfo.forms import CustomerForm, ProductForm, ShoppingCartForm, CartItemForm, OrderForm, OrderProductForm
from productinfo.models import (
	Customer,
	Product,
	Shopping_Cart,
	Cart_Item,
	Order,
	Order_Product,

)


class CustomerList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Customer
	permission_required = 'productinfo.view_customer'


class CustomerDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	model = Customer
	permission_required = 'productinfo.view_customer'

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		customer = self.get_object()
		shipping_method = customer.sm_id
		payment_method = customer.pm_id
		order_list = customer.orders.all()
		shopping_cart = customer.shopping_carts.all()
		context['shipping_method'] = shipping_method
		context['payment_method'] = payment_method
		context['order_list'] = order_list
		context['shopping_cart'] = shopping_cart
		return context


class CustomerCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	form_class = CustomerForm
	model = Customer
	permission_required = 'productinfo.add_customer'


class CustomerUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	form_class = CustomerForm
	model = Customer
	template_name = 'productinfo/customer_form_update.html'
	permission_required = 'productinfo.change_customer'


class CustomerDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Customer
	success_url = reverse_lazy('productinfo_customer_list_urlpattern')
	permission_required = 'productinfo.delete_customer'

	def get(self, request, pk):
		customer = get_object_or_404(Customer, pk=pk)
		orders = customer.orders.all()
		shopping_cart = customer.shopping_carts.all()

		if orders.count() > 0 or shopping_cart.count() > 0:
			return render(
				request,
				'productinfo/customer_refuse_delete.html',
				{'customer': customer,
				 'orders': orders,
				 'shopping_cart': shopping_cart,
				 }
			)
		else:
			return render(
				request,
				'productinfo/customer_confirm_delete.html',
				{'customer': customer}
			)


class ProductList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Product
	permission_required = 'productinfo.view_product'


class ProductDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	model = Product
	permission_required = 'productinfo.view_product'

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		product = self.get_object()
		category = product.category_id
		context['category'] = category
		return context


class ProductCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	form_class = ProductForm
	model = Product
	permission_required = 'productinfo.add_product'


class ProductUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	form_class = ProductForm
	model = Product
	template_name = 'productinfo/product_form_update.html'
	permission_required = 'productinfo.change_product'


class ProductDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Product
	success_url = reverse_lazy('productinfo_product_list_urlpattern')
	permission_required = 'productinfo.delete_product'

	def get(self, request, pk):
		product = get_object_or_404(Product, pk=pk)
		cartitem = product.cart_items.all()
		orderproduct = product.order_products.all()

		if orderproduct.count() > 0 or cartitem.count() > 0:
			return render(
				request,
				'productinfo/product_refuse_delete.html',
				{'product':product,
				 'cartitem': cartitem,
				 'orderproduct':orderproduct,

				}
			)
		else:
			return render(
				request,
				'productinfo/product_confirm_delete.html',
				{'product': product}
			)


class ShoppingCartList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Shopping_Cart
	permission_required = 'productinfo.view_shopping_cart'


class ShoppingCartDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	model = Shopping_Cart
	permission_required = 'productinfo.view_shopping_cart'

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		shopping_cart = self.get_object()
		customer_id = shopping_cart.customer_id
		shipping_method = shopping_cart.sm_id
		payment_method = shopping_cart.pm_id
		sc_list = shopping_cart.cart_items.all()

		total = 0
		for product in sc_list:
			total = product.quantity * product.product_id.product_price + total

		context['customer_id'] = customer_id
		context['shipping_method'] = shipping_method
		context['payment_method'] = payment_method
		context['sc_list'] = sc_list
		context['total'] = total
		return context


class ShoppingCartUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	form_class = ShoppingCartForm
	model = Shopping_Cart
	template_name = 'productinfo/shopping_cart_form_update.html'
	permission_required = 'productinfo.change_shopping_cart'


class ShoppingCartCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	form_class = ShoppingCartForm
	model = Shopping_Cart
	permission_required = 'productinfo.add_shopping_cart'


class ShoppingCartDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Shopping_Cart
	success_url = reverse_lazy('productinfo_shopping_cart_list_urlpattern')
	permission_required = 'productinfo.delete_shopping_cart'

	def get(self, request, pk):
		shopping_cart = get_object_or_404(Shopping_Cart, pk=pk)
		sc_list = shopping_cart.cart_items.all()
		if sc_list.count() > 0:
			return render(
				request,
				'productinfo/shopping_cart_refuse_delete.html',
				{'shopping_cart': shopping_cart,
				 'sc_list': sc_list,
				 }
			)
		else:
			return render(
				request,
				'productinfo/shoppingcart_confirm_delete.html',
				{'shopping_cart': shopping_cart}
			)


class CartItemList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Cart_Item
	permission_required = 'productinfo.view_cart_item'


class CartItemDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	model = Cart_Item
	permission_required = 'productinfo.view_cart_item'

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		cart_item = self.get_object()
		cart_id = cart_item.cart_id
		product_id = cart_item.product_id
		sub_total = cart_item.quantity * cart_item.product_id.product_price
		context['cart_id'] = cart_id
		context['product_id'] = product_id
		context['sub_total'] = sub_total
		return context


class CartItemCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	form_class = CartItemForm
	model = Cart_Item
	permission_required = 'productinfo.add_cart_item'


class CartItemUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	form_class = CartItemForm
	model = Cart_Item
	template_name = 'productinfo/cart_item_form_update.html'
	permission_required = 'productinfo.change_cart_item'


class CartItemDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Cart_Item
	success_url = reverse_lazy('productinfo_cart_item_list_urlpattern')
	permission_required = 'productinfo.delete_cart_item'


class OrderList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Order
	permission_required = 'productinfo.view_order'


class OrderDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	model = Order
	permission_required = 'productinfo.view_order'

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		order = self.get_object()
		customer_id = order.customer_id
		shipping_method = order.sm_id
		payment_method = order.pm_id
		product_list = order.order_products.all()

		total = 0
		for product in product_list:
			total = product.quantity * product.product_id.product_price + total

		context['customer_id'] = customer_id
		context['shipping_method'] = shipping_method
		context['payment_method'] = payment_method
		context['product_list'] = product_list
		context['total'] = total
		return context


class OrderCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	form_class = OrderForm
	model = Order
	permission_required = 'productinfo.add_order'


class OrderUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	form_class = OrderForm
	model = Order
	template_name = 'productinfo/order_form_update.html'
	permission_required = 'productinfo.change_order'


class OrderDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Order
	success_url = reverse_lazy('productinfo_order_list_urlpattern')
	permission_required = 'productinfo.delete_order'

	def get(self, request, pk):
		order = get_object_or_404(Order, pk=pk)
		op_list = order.order_products.all()
		if op_list.count() > 0:
			return render(
				request,
				'productinfo/order_refuse_delete.html',
				{'order': order,
				 'op_list': op_list,
				 }
			)
		else:
			return render(
				request,
				'productinfo/order_confirm_delete.html',
				{'order': order}
			)


class OrderProductList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Order_Product
	permission_required = 'productinfo.view_order_product'


class OrderProductDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	model = Order_Product
	permission_required = 'productinfo.view_order_product'

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		order_product = self.get_object()
		order_id = order_product.order_id
		product_id = order_product.product_id
		sub_total = order_product.quantity * order_product.product_id.product_price
		context['order_id'] = order_id
		context['product_id'] = product_id
		context['sub_total'] = sub_total
		return context


class OrderProductCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	form_class = OrderProductForm
	model = Order_Product
	permission_required = 'productinfo.add_order_product'


class OrderProductUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	form_class = OrderProductForm
	model = Order_Product
	template_name = 'productinfo/order_product_form_update.html'
	permission_required = 'productinfo.change_order_product'


class OrderProductDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Order_Product
	success_url = reverse_lazy('productinfo_order_product_list_urlpattern')
	permission_required = 'productinfo.delete_order_product'

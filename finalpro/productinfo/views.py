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


class CustomerList(ListView):
	model = Customer


class CustomerDetail(DetailView):
	model = Customer

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


class CustomerCreate(CreateView):
	form_class = CustomerForm
	model = Customer


class CustomerUpdate(UpdateView):
	form_class = CustomerForm
	model = Customer
	template_name = 'productinfo/customer_form_update.html'


class CustomerDelete(DeleteView):
	model = Customer
	success_url = reverse_lazy('productinfo_customer_list_urlpattern')

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


class ProductList(ListView):
	model = Product


class ProductDetail(DetailView):
	model = Product

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		product = self.get_object()
		category = product.category_id
		context['category'] = category
		return context


class ProductCreate(CreateView):
	form_class = ProductForm
	model = Product


class ProductUpdate(UpdateView):
	form_class = ProductForm
	model = Product
	template_name = 'productinfo/product_form_update.html'


class ProductDelete(DeleteView):
	model = Product
	success_url = reverse_lazy('productinfo_product_list_urlpattern')

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


class ShoppingCartList(View):

	def get(self, request):
		return render(
			request,
			'productinfo/shopping_cart_list.html',
			{'shoppingcart_list': Shopping_Cart.objects.all()}
		)


class ShoppingCartList(ListView):
	model = Shopping_Cart


# class ShoppingCartDetail(View):
#
# 	def get(self, request, pk):
# 		shopping_cart = get_object_or_404(
# 			Shopping_Cart,
# 			pk=pk
# 		)
# 		customer_id = shopping_cart.customer_id
# 		shipping_method = shopping_cart.sm_id
# 		payment_method = shopping_cart.pm_id
# 		sc_list = shopping_cart.cart_items.all()
#
# 		total = 0
# 		for product in sc_list:
# 			total = product.quantity * product.product_id.product_price + total
#
# 		return render(
# 			request,
# 			'productinfo/shopping_cart_detail.html',
# 			{'shopping_cart': shopping_cart,
# 			 'customer_id': customer_id,
# 			 'shipping_method': shipping_method,
# 			 'payment_method': payment_method,
# 			 'sc_list': sc_list,
# 			 'total': total}
# 		)
class ShoppingCartDetail(DetailView):
	model = Shopping_Cart

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


# class ShoppingCartUpdate(View):
# 	form_class = ShoppingCartForm
# 	model = Shopping_Cart
# 	template_name = 'productinfo/shopping_cart_form_update.html'
#
# 	def get_object(self, pk):
# 		return get_object_or_404(
# 			self.model,
# 			pk=pk)
#
# 	def get(self, request, pk):
# 		shopping_cart = self.get_object(pk)
# 		context = {
# 			'form': self.form_class(
# 				instance=shopping_cart),
# 			'product': shopping_cart,
# 		}
# 		return render(
# 			request, self.template_name, context)
#
# 	def post(self, request, pk):
# 		shopping_cart = self.get_object(pk)
# 		bound_form = self.form_class(
# 			request.POST, instance=shopping_cart)
# 		if bound_form.is_valid():
# 			new_shoppingcart = bound_form.save()
# 			return redirect(new_shoppingcart)
# 		else:
# 			context = {
# 				'form': bound_form,
# 				'shopping_cart': shopping_cart,
# 			}
# 			return render(
# 				request,
# 				self.template_name,
# 				context)
class ShoppingCartUpdate(UpdateView):
	form_class = ShoppingCartForm
	model = Shopping_Cart
	template_name = 'productinfo/shopping_cart_form_update.html'


# class ShoppingCartCreate(ObjectCreateMixin, View):
# 	form_class = ShoppingCartForm
# 	template_name = 'productinfo/shopping_cart_form.html'
class ShoppingCartCreate(CreateView):
	form_class = ShoppingCartForm
	model = Shopping_Cart


class ShoppingCartDelete(DeleteView):
	model = Shopping_Cart
	success_url = reverse_lazy('productinfo_shopping_cart_list_urlpattern')

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


# class CartItemList(View):
#
# 	def get(self, request):
# 		return render(
# 			request,
# 			'productinfo/cart_item_list.html',
# 			{'cartitem_list': Cart_Item.objects.all()}
# 		)
class CartItemList(ListView):
	model = Cart_Item


# class CartItemDetail(View):
#
# 	def get(self, request, pk):
# 		cartitem = get_object_or_404(
# 			Cart_Item,
# 			pk=pk
# 		)
# 		cart_id = cartitem.cart_id
# 		product_id = cartitem.product_id
#
# 		sub_total = cartitem.quantity * cartitem.product_id.product_price
# 		return render(
# 			request,
# 			'productinfo/cart_item_detail.html',
# 			{'cartitem': cartitem, 'cart_id': cart_id, 'product_id': product_id, 'sub_total': sub_total}
# 		)
class CartItemDetail(DetailView):
	model = Cart_Item

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


# class CartItemCreate(ObjectCreateMixin, View):
# 	form_class = CartItemForm
# 	template_name = 'productinfo/cart_item_form.html'
class CartItemCreate(CreateView):
	form_class = CartItemForm
	model = Cart_Item


# class CartItemUpdate(View):
# 	form_class = CartItemForm
# 	model = Cart_Item
# 	template_name = 'productinfo/cart_item_form_update.html'
#
# 	def get_object(self, pk):
# 		return get_object_or_404(
# 			self.model,
# 			pk=pk)
#
# 	def get(self, request, pk):
# 		cart_item = self.get_object(pk)
# 		context = {
# 			'form': self.form_class(
# 				instance=cart_item),
# 			'cart_item': cart_item,
# 		}
# 		return render(
# 			request, self.template_name, context)
#
# 	def post(self, request, pk):
# 		cart_item = self.get_object(pk)
# 		bound_form = self.form_class(
# 			request.POST, instance=cart_item)
# 		if bound_form.is_valid():
# 			new_cartitem = bound_form.save()
# 			return redirect(new_cartitem)
# 		else:
# 			context = {
# 				'form': bound_form,
# 				'cart_item': cart_item,
# 			}
# 			return render(
# 				request,
# 				self.template_name,
# 				context)
class CartItemUpdate(UpdateView):
	form_class = CartItemForm
	model = Cart_Item
	template_name = 'productinfo/cart_item_form_update.html'


# class CartItemDelete(View):
#
# 	def get(self, request, pk):
# 		cart_item = self.get_object(pk)
# 		return render(
# 			request,
# 			'productinfo/cart_item_confirm_delete.html',
# 			{'cart_item': cart_item}
# 		)
#
# 	def get_object(self, pk):
# 		cart_item = get_object_or_404(
# 			Cart_Item,
# 			pk=pk
# 		)
# 		return cart_item
#
# 	def post(self, request, pk):
# 		cart_item = self.get_object(pk)
# 		cart_item.delete()
# 		return redirect('productinfo_cartitem_list_urlpattern')
class CartItemDelete(DeleteView):
	model = Cart_Item
	success_url = reverse_lazy('productinfo_cart_item_list_urlpattern')


class OrderList(ListView):
	model = Order


class OrderDetail(DetailView):
	model = Order

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


class OrderCreate(CreateView):
	form_class = OrderForm
	model = Order


class OrderUpdate(UpdateView):
	form_class = OrderForm
	model = Order
	template_name = 'productinfo/order_form_update.html'


class OrderDelete(DeleteView):
	model = Order
	success_url = reverse_lazy('productinfo_order_list_urlpattern')

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



# class OrderProductList(View):
#
# 	def get(self, request):
# 		return render(
# 			request,
# 			'productinfo/order_product_list.html',
# 			{'orderproduct_list': Order_Product.objects.all()}
# 		)
class OrderProductList(ListView):
	model = Order_Product


# class OrderProductDetail(View):
#
# 	def get(self, request, pk):
# 		orderproduct = get_object_or_404(
# 			Order_Product,
# 			pk=pk
# 		)
# 		order_id = orderproduct.order_id
# 		product_id = orderproduct.product_id
# 		return render(
# 			request,
# 			'productinfo/order_product_detail.html',
# 			{'orderproduct': orderproduct,
# 			 'order_id': order_id,
# 			 'product_id': product_id}
# 		)
class OrderProductDetail(DetailView):
	model = Order_Product

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


# class OrderProductCreate(ObjectCreateMixin, View):
# 	form_class = OrderProductForm
# 	template_name = 'productinfo/order_product_form.html'
class OrderProductCreate(CreateView):
	form_class = OrderProductForm
	model = Order_Product


# class OrderProductUpdate(View):
# 	form_class = OrderProductForm
# 	model = Order_Product
# 	template_name = 'productinfo/order_product_form_update.html'
#
# 	def get_object(self, pk):
# 		return get_object_or_404(
# 			self.model,
# 			pk=pk)
#
# 	def get(self, request, pk):
# 		orderproduct = self.get_object(pk)
# 		context = {
# 			'form': self.form_class(
# 				instance=orderproduct),
# 			'orderproduct': orderproduct,
# 		}
# 		return render(
# 			request, self.template_name, context)
#
# 	def post(self, request, pk):
# 		orderproduct = self.get_object(pk)
# 		bound_form = self.form_class(
# 			request.POST, instance=orderproduct)
# 		if bound_form.is_valid():
# 			new_orderproduct = bound_form.save()
# 			return redirect(new_orderproduct)
# 		else:
# 			context = {
# 				'form': bound_form,
# 				'orderproduct': orderproduct,
# 			}
# 			return render(
# 				request,
# 				self.template_name,
# 				context)
class OrderProductUpdate(UpdateView):
	form_class = OrderProductForm
	model = Order_Product
	template_name = 'productinfo/order_product_form_update.html'


# class OrderProductDelete(View):
#
# 	def get(self, request, pk):
# 		orderproduct = self.get_object(pk)
# 		return render(
# 			request,
# 			'productinfo/order_product_confirm_delete.html',
# 			{'orderproduct': orderproduct}
# 		)
#
# 	def get_object(self, pk):
# 		orderproduct = get_object_or_404(
# 			Order_Product,
# 			pk=pk
# 		)
# 		return orderproduct
#
# 	def post(self, request, pk):
# 		orderproduct = self.get_object(pk)
# 		orderproduct.delete()
# 		return redirect('productinfo_orderproduct_list_urlpattern')
class OrderProductDelete(DeleteView):
	model = Order_Product
	success_url = reverse_lazy('productinfo_order_product_list_urlpattern')

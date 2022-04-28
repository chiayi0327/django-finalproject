from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from productinfo.forms import CustomerForm, ProductForm, ShoppingCartForm, CartItemForm, OrderForm, OrderProductForm
from productinfo.models import (
	Customer,
	Product,
	Shopping_Cart,
	Cart_Item,
	Order,
	Order_Product,

)
from productinfo.utils import ObjectCreateMixin


class CustomerList(ListView):
	model = Customer


class CustomerDetail(View):

	def get(self, request, pk):
		customer = get_object_or_404(
			Customer,
			pk=pk
		)
		shipping_method = customer.sm_id
		payment_method = customer.pm_id
		order_list = customer.orders.all()
		shopping_cart = customer.shopping_carts.all()
		return render(
			request,
			'productinfo/customer_detail.html',
			{'customer': customer,
			 'shipping_method': shipping_method,
			 'payment_method': payment_method,
			 'order_list': order_list,
			 'shopping_cart': shopping_cart}
		)


class CustomerCreate(ObjectCreateMixin, View):
	form_class = CustomerForm
	template_name = 'productinfo/customer_form.html'


class CustomerUpdate(View):
	form_class = CustomerForm
	model = Customer
	template_name = 'productinfo/customer_form_update.html'

	def get_object(self, pk):
		return get_object_or_404(
			self.model,
			pk=pk)

	def get(self, request, pk):
		customer = self.get_object(pk)
		context = {
			'form': self.form_class(
				instance=customer),
			'customer': customer,
		}
		return render(
			request, self.template_name, context)

	def post(self, request, pk):
		customer = self.get_object(pk)
		bound_form = self.form_class(
			request.POST, instance=customer)
		if bound_form.is_valid():
			new_customer = bound_form.save()
			return redirect(new_customer)
		else:
			context = {
				'form': bound_form,
				'customer': customer,
			}
			return render(
				request,
				self.template_name,
				context)


class CustomerDelete(View):

	def get(self, request, pk):
		customer = self.get_object(pk)
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

	def get_object(self, pk):
		return get_object_or_404(
			Customer,
			pk=pk)

	def post(self, request, pk):
		customer = self.get_object(pk)
		customer.delete()
		return redirect('productinfo_customer_list_urlpattern')


class ProductList(ListView):
	model = Product


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


class ProductCreate(ObjectCreateMixin, View):
	form_class = ProductForm
	template_name = 'productinfo/product_form.html'


class ProductUpdate(View):
	form_class = ProductForm
	model = Product
	template_name = 'productinfo/product_form_update.html'

	def get_object(self, pk):
		return get_object_or_404(
			self.model,
			pk=pk)

	def get(self, request, pk):
		product = self.get_object(pk)
		context = {
			'form': self.form_class(
				instance=product),
			'product': product,
		}
		return render(
			request, self.template_name, context)

	def post(self, request, pk):
		product = self.get_object(pk)
		bound_form = self.form_class(
			request.POST, instance=product)
		if bound_form.is_valid():
			new_product = bound_form.save()
			return redirect(new_product)
		else:
			context = {
				'form': bound_form,
				'product': product,
			}
			return render(
				request,
				self.template_name,
				context)


class ProductDelete(View):

	def get(self, request, pk):
		product = self.get_object(pk)
		return render(
			request,
			'productinfo/product_confirm_delete.html',
			{'product': product}
		)

	def get_object(self, pk):
		product = get_object_or_404(
			Product,
			pk=pk
		)
		return product

	def post(self, request, pk):
		product = self.get_object(pk)
		product.delete()
		return redirect('productinfo_product_list_urlpattern')


class ShoppingCartList(View):

	def get(self, request):
		return render(
			request,
			'productinfo/shoppingcart_list.html',
			{'shoppingcart_list': Shopping_Cart.objects.all()}
		)


class ShoppingCartDetail(View):

	def get(self, request, pk):
		shopping_cart = get_object_or_404(
			Shopping_Cart,
			pk=pk
		)
		customer_id = shopping_cart.customer_id
		shipping_method = shopping_cart.sm_id
		payment_method = shopping_cart.pm_id
		sc_list = shopping_cart.cart_items.all()

		total = 0
		for product in sc_list:
			total = product.quantity * product.product_id.product_price + total

		return render(
			request,
			'productinfo/shoppingcart_detail.html',
			{'shopping_cart': shopping_cart,
			 'customer_id': customer_id,
			 'shipping_method': shipping_method,
			 'payment_method': payment_method,
			 'sc_list': sc_list,
			 'total': total}
		)


class ShoppingCartUpdate(View):
	form_class = ShoppingCartForm
	model = Shopping_Cart
	template_name = 'productinfo/shoppingcart_form_update.html'

	def get_object(self, pk):
		return get_object_or_404(
			self.model,
			pk=pk)

	def get(self, request, pk):
		shopping_cart = self.get_object(pk)
		context = {
			'form': self.form_class(
				instance=shopping_cart),
			'product': shopping_cart,
		}
		return render(
			request, self.template_name, context)

	def post(self, request, pk):
		shopping_cart = self.get_object(pk)
		bound_form = self.form_class(
			request.POST, instance=shopping_cart)
		if bound_form.is_valid():
			new_shoppingcart = bound_form.save()
			return redirect(new_shoppingcart)
		else:
			context = {
				'form': bound_form,
				'shopping_cart': shopping_cart,
			}
			return render(
				request,
				self.template_name,
				context)


class ShoppingCartCreate(ObjectCreateMixin, View):
	form_class = ShoppingCartForm
	template_name = 'productinfo/shoppingcart_form.html'


class ShoppingCartDelete(View):

	def get(self, request, pk):
		shopping_cart = self.get_object(pk)
		sc_list = shopping_cart.cart_items.all()
		if sc_list.count() > 0:
			return render(
				request,
				'productinfo/shoppingcart_refuse_delete.html',
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

	def get_object(self, pk):
		shopping_cart = get_object_or_404(
			Shopping_Cart,
			pk=pk
		)
		return shopping_cart

	def post(self, request, pk):
		shopping_cart = self.get_object(pk)
		shopping_cart.delete()
		return redirect('productinfo_shoppingcart_list_urlpattern')


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

		sub_total = cartitem.quantity * cartitem.product_id.product_price
		return render(
			request,
			'productinfo/cartitem_detail.html',
			{'cartitem': cartitem, 'cart_id': cart_id, 'product_id': product_id, 'sub_total': sub_total}
		)


class CartItemCreate(ObjectCreateMixin, View):
	form_class = CartItemForm
	template_name = 'productinfo/cartitem_form.html'


class CartItemUpdate(View):
	form_class = CartItemForm
	model = Cart_Item
	template_name = 'productinfo/cartitem_form_update.html'

	def get_object(self, pk):
		return get_object_or_404(
			self.model,
			pk=pk)

	def get(self, request, pk):
		cart_item = self.get_object(pk)
		context = {
			'form': self.form_class(
				instance=cart_item),
			'cart_item': cart_item,
		}
		return render(
			request, self.template_name, context)

	def post(self, request, pk):
		cart_item = self.get_object(pk)
		bound_form = self.form_class(
			request.POST, instance=cart_item)
		if bound_form.is_valid():
			new_cartitem = bound_form.save()
			return redirect(new_cartitem)
		else:
			context = {
				'form': bound_form,
				'cart_item': cart_item,
			}
			return render(
				request,
				self.template_name,
				context)


class CartItemDelete(View):

	def get(self, request, pk):
		cart_item = self.get_object(pk)
		return render(
			request,
			'productinfo/cartitem_confirm_delete.html',
			{'cart_item': cart_item}
		)

	def get_object(self, pk):
		cart_item = get_object_or_404(
			Cart_Item,
			pk=pk
		)
		return cart_item

	def post(self, request, pk):
		cart_item = self.get_object(pk)
		cart_item.delete()
		return redirect('productinfo_cartitem_list_urlpattern')


class OrderList(ListView):
	model = Order


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
			 'customer_id': customer_id,
			 'shipping_method': shipping_method,
			 'payment_method': payment_method,
			 'product_list': product_list}
		)


class OrderCreate(ObjectCreateMixin, View):
	form_class = OrderForm
	template_name = 'productinfo/order_form.html'


class OrderUpdate(View):
	form_class = OrderForm
	model = Order
	template_name = 'productinfo/order_form_update.html'

	def get_object(self, pk):
		return get_object_or_404(
			self.model,
			pk=pk)

	def get(self, request, pk):
		order = self.get_object(pk)
		context = {
			'form': self.form_class(
				instance=order),
			'order': order,
		}
		return render(
			request, self.template_name, context)

	def post(self, request, pk):
		order = self.get_object(pk)
		bound_form = self.form_class(
			request.POST, instance=order)
		if bound_form.is_valid():
			new_order = bound_form.save()
			return redirect(new_order)
		else:
			context = {
				'form': bound_form,
				'order': order,
			}
			return render(
				request,
				self.template_name,
				context)


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


class OrderDelete(View):

	def get(self, request, pk):
		order = self.get_object(pk)
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

	def get_object(self, pk):
		order = get_object_or_404(
			Order,
			pk=pk
		)
		return order

	def post(self, request, pk):
		order = self.get_object(pk)
		order.delete()
		return redirect('productinfo_order_list_urlpattern')


class OrderProductCreate(ObjectCreateMixin, View):
	form_class = OrderProductForm
	template_name = 'productinfo/orderproduct_form.html'


class OrderProductUpdate(View):
	form_class = OrderProductForm
	model = Order_Product
	template_name = 'productinfo/orderproduct_form_update.html'

	def get_object(self, pk):
		return get_object_or_404(
			self.model,
			pk=pk)

	def get(self, request, pk):
		orderproduct = self.get_object(pk)
		context = {
			'form': self.form_class(
				instance=orderproduct),
			'orderproduct': orderproduct,
		}
		return render(
			request, self.template_name, context)

	def post(self, request, pk):
		orderproduct = self.get_object(pk)
		bound_form = self.form_class(
			request.POST, instance=orderproduct)
		if bound_form.is_valid():
			new_orderproduct = bound_form.save()
			return redirect(new_orderproduct)
		else:
			context = {
				'form': bound_form,
				'orderproduct': orderproduct,
			}
			return render(
				request,
				self.template_name,
				context)


class OrderProductDelete(View):

	def get(self, request, pk):
		orderproduct = self.get_object(pk)
		return render(
			request,
			'productinfo/orderproduct_confirm_delete.html',
			{'orderproduct': orderproduct}
		)

	def get_object(self, pk):
		orderproduct = get_object_or_404(
			Order_Product,
			pk=pk
		)
		return orderproduct

	def post(self, request, pk):
		orderproduct = self.get_object(pk)
		orderproduct.delete()
		return redirect('productinfo_orderproduct_list_urlpattern')

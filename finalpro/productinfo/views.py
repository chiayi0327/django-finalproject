from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

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
		shoppingcart = get_object_or_404(
			Shopping_Cart,
			pk=pk
		)
		customer_id = shoppingcart.customer_id
		shipping_method = shoppingcart.sm_id
		payment_method = shoppingcart.pm_id
		sc_list = shoppingcart.cart_items.all()

		total = 0
		for product in sc_list:
			total = product.quantity * product.product_id.product_price + total

		return render(
			request,
			'productinfo/shoppingcart_detail.html',
			{'shoppingcart': shoppingcart,
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

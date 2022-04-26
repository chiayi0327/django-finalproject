from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse


class Category(models.Model):
	category_id = models.AutoField(primary_key=True)
	category_name = models.CharField(max_length=45, unique=True)
	category_description = models.CharField(max_length=225)

	def __str__(self):
		return f'{self.category_name}'

	class Meta:
		ordering = ['category_name']
		constraints = [
			UniqueConstraint(fields=['category_name'], name='unique_category')
		]


class Shipping_Method(models.Model):
	sm_id = models.AutoField(primary_key=True)
	sm_name = models.CharField(max_length=45, unique=True)
	sm_description = models.CharField(max_length=225)

	def __str__(self):
		return f'{self.sm_name}'

	class Meta:
		ordering = ['sm_name']
		constraints = [
			UniqueConstraint(fields=['sm_name'], name='unique_sm')
		]


class Payment_Method(models.Model):
	pm_id = models.AutoField(primary_key=True)
	pm_name = models.CharField(max_length=45, unique=True)
	pm_description = models.CharField(max_length=225)

	def __str__(self):
		return f'{self.pm_name}'

	class Meta:
		ordering = ['pm_name']
		constraints = [
			UniqueConstraint(fields=['pm_name'], name='unique_pm')
		]


class Customer(models.Model):
	customer_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	disambiguator = models.CharField(max_length=45, blank=True, default='')
	username = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
	email = models.CharField(max_length=225)
	sm_id = models.ForeignKey(Shipping_Method, related_name='customers', on_delete=models.PROTECT)
	pm_id = models.ForeignKey(Payment_Method, related_name='customers', on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.username} - {self.email}'

	def get_absolute_url(self):
		return reverse('productinfo_customer_detail_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_update_url(self):
		return reverse('productinfo_customer_update_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_delete_url(self):
		return reverse('productinfo_customer_delete_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	class Meta:
		ordering = ['customer_id']
		constraints = [
			UniqueConstraint(fields=['username', 'email', 'disambiguator'], name='unique_customer')
		]


class Product(models.Model):
	product_id = models.AutoField(primary_key=True)
	product_name = models.CharField(max_length=225, unique=True)
	product_price = models.FloatField()
	stock_num = models.IntegerField()
	category_id = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.product_id} - {self.product_name}'

	def get_absolute_url(self):
		return reverse('productinfo_product_detail_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_update_url(self):
		return reverse('productinfo_product_update_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_delete_url(self):
		return reverse('productinfo_product_delete_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	class Meta:
		ordering = ['product_id']
		constraints = [
			UniqueConstraint(fields=['product_name'], name='unique_product')
		]


class Shopping_Cart(models.Model):
	cart_id = models.AutoField(primary_key=True)
	total_price = models.FloatField()
	customer_id = models.ForeignKey(Customer, related_name='shopping_carts', on_delete=models.PROTECT)
	sm_id = models.ForeignKey(Shipping_Method, related_name='shopping_carts', on_delete=models.PROTECT)
	pm_id = models.ForeignKey(Payment_Method, related_name='shopping_carts', on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.cart_id} - {self.customer_id}'

	def get_absolute_url(self):
		return reverse('productinfo_shoppingcart_detail_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_update_url(self):
		return reverse('productinfo_shoppingcart_update_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_delete_url(self):
		return reverse('productinfo_shoppingcart_delete_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	class Meta:
		ordering = ['cart_id']
		constraints = [
			UniqueConstraint(fields=['customer_id'], name='unique_shoppingcart')
		]


class Cart_Item(models.Model):
	ci_id = models.AutoField(primary_key=True)
	quantity = models.IntegerField()
	cart_id = models.ForeignKey(Shopping_Cart, related_name='cart_items', on_delete=models.PROTECT)
	product_id = models.ForeignKey(Product, related_name='cart_items', on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.cart_id} - {self.product_id}'

	def get_absolute_url(self):
		return reverse('productinfo_cartitem_detail_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_update_url(self):
		return reverse('productinfo_cartitem_update_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_delete_url(self):
		return reverse('productinfo_cartitem_delete_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	class Meta:
		ordering = ['cart_id', 'product_id']
		constraints = [
			UniqueConstraint(fields=['cart_id', 'product_id'], name='unique_cartitem')
		]


class Order(models.Model):
	order_id = models.AutoField(primary_key=True)
	total_price = models.FloatField()
	order_date = models.DateTimeField()
	receiver = models.CharField(max_length=45)
	address = models.CharField(max_length=225)
	sm_id = models.ForeignKey(Shipping_Method, related_name='orders', on_delete=models.PROTECT)
	pm_id = models.ForeignKey(Payment_Method, related_name='orders', on_delete=models.PROTECT)
	customer_id = models.ForeignKey(Customer, related_name='orders', on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.order_id} - {self.order_date} - {self.total_price}'

	def get_absolute_url(self):
		return reverse('productinfo_order_detail_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_update_url(self):
		return reverse('productinfo_order_update_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_delete_url(self):
		return reverse('productinfo_order_delete_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	class Meta:
		ordering = ['order_date', 'order_id']
		constraints = [
			UniqueConstraint(fields=['order_id'], name='unique_order')
		]


class Order_Product(models.Model):
	oitem_id = models.AutoField(primary_key=True)
	price = models.FloatField()
	quantity = models.IntegerField()
	order_id = models.ForeignKey(Order, related_name='order_products', on_delete=models.PROTECT)
	product_id = models.ForeignKey(Product, related_name='order_products', on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.order_id} - {self.product_id}'

	def get_absolute_url(self):
		return reverse('productinfo_orderproduct_detail_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_update_url(self):
		return reverse('productinfo_orderproduct_update_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	def get_delete_url(self):
		return reverse('productinfo_orderproduct_delete_urlpattern',
					   kwargs={'pk':self.pk}
					   )

	class Meta:
		ordering = ['order_id']
		constraints = [
			UniqueConstraint(fields=['oitem_id', 'order_id', 'product_id'], name='unique_orderproduct')
		]

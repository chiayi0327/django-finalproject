from __future__ import unicode_literals
from itertools import chain

from django.db import migrations


def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    category_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                             content_type__model='category')

    shipping_method_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                          content_type__model='shipping_method')

    payment_method_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                                  content_type__model='payment_method')

    customer_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                                  content_type__model='customer')

    product_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                           content_type__model='product')

    shopping_cart_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                         content_type__model='shopping_cart')

    cart_item_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                          content_type__model='cart_item')

    order_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                               content_type__model='order')

    order_product_permissions = permission_class.objects.filter(content_type__app_label='productinfo',
                                                               content_type__model='order_product')

    perm_view_category = permission_class.objects.filter(content_type__app_label='productinfo',
                                                           content_type__model='category',
                                                           codename='view_category')

    perm_view_shipping_method = permission_class.objects.filter(content_type__app_label='productinfo',
                                                        content_type__model='shipping_method',
                                                        codename='view_shipping_method')

    perm_view_payment_method = permission_class.objects.filter(content_type__app_label='productinfo',
                                                               content_type__model='payment_method',
                                                               codename='view_payment_method')

    perm_view_customer = permission_class.objects.filter(content_type__app_label='productinfo',
                                                               content_type__model='customer',
                                                               codename='view_customer')

    perm_view_product = permission_class.objects.filter(content_type__app_label='productinfo',
                                                         content_type__model='product',
                                                         codename='view_product')

    perm_view_shopping_cart = permission_class.objects.filter(content_type__app_label='productinfo',
                                                       content_type__model='shopping_cart',
                                                       codename='view_shopping_cart')

    perm_view_cart_item = permission_class.objects.filter(content_type__app_label='productinfo',
                                                        content_type__model='cart_item',
                                                        codename='view_cart_item')

    perm_view_order = permission_class.objects.filter(content_type__app_label='productinfo',
                                                             content_type__model='order',
                                                             codename='view_order')

    perm_view_order_product = permission_class.objects.filter(content_type__app_label='productinfo',
                                                             content_type__model='order_product',
                                                             codename='view_order_product')

    pi_user_permissions = chain(perm_view_category,
                                perm_view_shipping_method,
                                perm_view_payment_method,
                                perm_view_customer,
                                perm_view_product,
                                perm_view_shopping_cart,
                                perm_view_cart_item,
                                perm_view_order,
                                perm_view_order_product)

    pi_admin_permissions = chain(category_permissions,
                                     shipping_method_permissions,
                                     payment_method_permissions,
                                     customer_permissions,
                                     product_permissions,
                                     shopping_cart_permissions,
                                     perm_view_cart_item,
                                     perm_view_order,
                                     perm_view_order_product)

    pi_customer_permissions = chain(cart_item_permissions,
                                     order_permissions,
                                     order_product_permissions,
                                     perm_view_category,
                                     perm_view_shipping_method,
                                     perm_view_payment_method,
                                     perm_view_customer,
                                     perm_view_product,
                                     perm_view_shopping_cart)

    my_groups_initialization_list = [
        {
            "name": "pi_user",
            "permissions_list": pi_user_permissions,
        },
        {
            "name": "pi_admin",
            "permissions_list": pi_admin_permissions,
        },
        {
            "name": "pi_customer",
            "permissions_list": pi_customer_permissions,
        },
    ]
    return my_groups_initialization_list


def add_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            group_object.permissions.set(group['permissions_list'])
            group_object.save()


def remove_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            list_of_permissions = group['permissions_list']
            for permission in list_of_permissions:
                group_object.permissions.remove(permission)
                group_object.save()


class Migration(migrations.Migration):
    dependencies = [
        ('productinfo', '0007_create_groups'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions_data,
            remove_group_permissions_data
        )
    ]

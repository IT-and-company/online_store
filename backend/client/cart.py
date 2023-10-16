from decimal import Decimal

from django.conf import settings

from client.models import CartProduct, UserCart
from products.models import VariationProduct


class Cart(object):

    def __init__(self, request, from_db=False):
        """
        Инициализируем корзину
        """
        if not from_db:
            self.session = request.session
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                # save an empty cart in the session
                cart = self.session[settings.CART_SESSION_ID] = {}
        else:
            self.user = request.user
            user_cart, _ = UserCart.objects.prefetch_related(
                'products'
            ).get_or_create(user=self.user)
            cart = {}
            user_cart_products = user_cart.products.select_related(
                'product'
            ).all()
            for cart_product in user_cart_products:
                if not cart_product.product.sale:
                    product_price = cart_product.product.price
                else:
                    product_price = cart_product.product.price * ((
                        100 - cart_product.product.sale) / 100)
            cart = {
                str(product.product.id): {
                    'quantity': product.quantity, 'price': product_price
                } for product in user_cart_products
            }
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': product.price}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        if self.cart[product_id]['quantity'] == 0:
            self.remove(product)
        self.save()

    def save(self):
        if hasattr(self, 'session'):
            # Обновление сессии cart
            self.session[settings.CART_SESSION_ID] = self.cart
            # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
            self.session.modified = True
        else:
            user_cart = UserCart.objects.get(user=self.user)
            for cart_product in user_cart.products.all():
                if str(cart_product.product.id) not in self.cart:
                    cart_product.delete()

            for product_id, product_data in self.cart.items():
                CartProduct.objects.update_or_create(
                    cart=user_cart,
                    product=VariationProduct.objects.get(id=product_id),
                    defaults={'quantity': product_data['quantity']}
                )

    def clear(self):
        if hasattr(self, 'session'):
            # удаление корзины из сессии
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True
        else:
            user_cart = UserCart.objects.get(user=self.user)
            for cart_product in user_cart.products.all():
                cart_product.delete()

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = list(self.cart.keys())
        # получение объектов product и добавление их в корзину
        products = VariationProduct.objects.filter(id__in=product_ids)
        if len(product_ids) > len(products):
            for item in product_ids:
                if not VariationProduct.objects.filter(id=item).exists():
                    self.cart.pop(item)
        for product in products:
            self.cart[str(product.id)]['variation'] = product
            if not product.sale:
                self.cart[str(product.id)]['price'] = product.price
                continue

            self.cart[str(product.id)]['price'] = Decimal(str(round(
                product.price * ((100 - product.sale) / 100))))

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            print(item)
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(
            item['price']) * item['quantity'] for item in self.cart.values())

from django.conf import settings
from django.db import models

# Create your models here.
from basketapp.models import Basket
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEED = 'PCD'
    PAID = 'PD'
    READY = 'RDY'
    DONE = 'DN'
    CANCEL = 'CNC'

    ORDER_STATUSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен на обработку'),
        (PROCEED, 'обработан'),
        (PAID, 'оплачен'),
        (READY, 'отов к выдаче'),
        (DONE, 'выдан'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменен")
    status = models.CharField(
        verbose_name='Статус',
        choices=ORDER_STATUSES,
        max_length=3,
        default=FORMING
    )
    is_active = models.BooleanField(default=True, verbose_name='активен', )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created_at',)

    def total_quantity(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, _items)))

    def total_cost(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, _items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

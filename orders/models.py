from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel, BaseModel


class PromoCode(TimeStampedModel):
    """
    Model to store promo codes.
    """
    name = models.CharField(_('name'), max_length=127)
    code = models.CharField(_('code'), max_length=127, unique=True)
    discount = models.PositiveIntegerField(_('discount'), validators=[MinValueValidator(1)])
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))

    class Meta:
        verbose_name = _('Promo-Code')
        verbose_name_plural = _('Promo-Code')
        ordering = ('-start_date',)

    @property
    def is_valid(self):
        return self.start_date <= timezone.now().date() <= self.end_date


class OrderProduct(BaseModel):
    """
    Model to store ordered product (individual).
    """
    DELIVERY_STATUS = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='ordered_products',
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        related_name='ordered'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.PROTECT,
        related_name='products'
    )
    color = models.CharField(_('color'), max_length=64, default='')
    quantity = models.PositiveIntegerField(_('quantity'), default=1, validators=[MinValueValidator(1)])
    rate = models.DecimalField(
        _('rate'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text=_(
            'price per product.'
        )
    )
    net_total = models.DecimalField(
        _('net total'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text=_(
            'price per product * quantity.'
        )
    )

    delivery_status = models.CharField(
        _('delivery status'),
        max_length=9,
        choices=DELIVERY_STATUS,
        default='Pending'
    )
    estimated_delivery_date = models.DateField(_('estimated delivery date'), default=None, null=True)
    delivered_at = models.DateField(_('delivered at'), default=None, null=True)

    to_be_reviewed = models.BooleanField(_('to be reviewed'), default=True)
    reviews = models.OneToOneField(
        'products.RatingAndReview',
        on_delete=models.SET_NULL,
        null=True,
        related_name='on_ordered_product'
    )

    class Meta:
        verbose_name='Order Product'
        verbose_name_plural='Order Products'


class Order(BaseModel):
    """
    Model to store order information.
    """
    DELIVERY_STATUS = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
    )
    payment = models.OneToOneField('payments.Payment', on_delete=models.PROTECT)
    delivery_status = models.CharField(
        _('delivery status'),
        max_length=9,
        choices=DELIVERY_STATUS,
        default='Pending'
    )
    estimated_delivery_date = models.DateField(_('estimated delivery date'), default=None, null=True)
    delivered_at = models.DateField(_('delivered at'), default=None, null=True)
    shipping = models.ForeignKey(
        'users.Shipping',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    order_uuid = models.CharField(_('order uuid'), max_length=255, unique=True)
    discount = models.DecimalField(
        _('discount'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_(
            'discount using promo code.'
        )
    )
    delivery_charge = models.DecimalField(
        _('delivery charge'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_(
            'discount using promo code.'
        )
    )
    final_price = models.DecimalField(
        _('final price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text=_(
            'final price of all products in cart.'
        )
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('-created_on',)
    
    def __str__(self):
        return f'{self.order_uuid}'


class PreOrderProductBundle(BaseModel):
    """
    Model to store pre-order information.
    """
    DELIVERY_STATUS = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='pre_orders',
    )
    product_bundle = models.ForeignKey(
        'products.ProductBundleForPreOrder',
        on_delete=models.SET_NULL,
        null=True,
        related_name='pre_orders'
    )
    quantity = models.PositiveIntegerField(_('quantity'), default=1, validators=[MinValueValidator(1)])
    rate = models.DecimalField(
        _('rate'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text=_(
            'price per product-bundle.'
        )
    )
    payment = models.OneToOneField('payments.Payment', on_delete=models.PROTECT, related_name='pre_order')
    delivery_status = models.CharField(
        _('delivery status'),
        max_length=9,
        choices=DELIVERY_STATUS,
        default='Pending'
    )
    estimated_delivery_date = models.DateField(_('estimated delivery date'), default=None, null=True)
    delivered_at = models.DateField(_('delivered at'), default=None, null=True)
    shipping = models.ForeignKey(
        'users.Shipping',
        on_delete=models.SET_NULL,
        null=True,
        related_name='pre_orders'
    )
    pre_order_uuid = models.CharField(_('pre order uuid'), max_length=255, unique=True)
    discount = models.DecimalField(
        _('discount'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_(
            'discount using promo code.'
        )
    )
    delivery_charge = models.DecimalField(
        _('delivery charge'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_(
            'shipping delivery charge.'
        )
    )
    final_price = models.DecimalField(
        _('final price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text=_(
            'final price of all products in bundle.'
        )
    )

    class Meta:
        verbose_name = _('Pre-Order Product Bundle')
        verbose_name_plural = _('Pre-Order Product Bundles')
        ordering = ('-created_on',)
    
    def __str__(self):
        return f'{self.pre_order_uuid}'

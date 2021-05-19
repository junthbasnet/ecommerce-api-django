from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel


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

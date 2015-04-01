from collections import namedtuple

from django.utils.timezone import now

from .models import Mask as MaskRecord

Mask = namedtuple('Mask', 'title subtitle image_url')

def get_active_mask():
    instant = now()
    records = tuple(MaskRecord
        .objects
        .order_by('-effective', 'expiration')
        .filter(
            effective__lte=instant,
            expiration__gte=instant,
        )[:1]
    )
    if not records:
        return None
    record = records[0]
    return _make_mask(record)

def _make_mask(record):
    return Mask(
        title=record.title,
        subtitle=record.subtitle,
        image_url=record.image
    )

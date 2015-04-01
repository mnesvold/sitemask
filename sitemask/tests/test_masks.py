from datetime import timedelta
from unittest.mock import patch, sentinel

from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.timezone import now

from sitemask.masks import _make_mask, get_active_mask, Mask as MaskData
from sitemask.models import Mask as MaskModel

class GetActiveMaskTests(TestCase):
    def test_empty_table(self):
        mask = get_active_mask()
        self.assertIsNone(mask)

    def test_past_entries(self):
        self._make_mask(
            effective = now() - timedelta(days=14),
            expiration = now() - timedelta(days=7),
        )
        mask = get_active_mask()
        self.assertIsNone(mask)

    def test_future_entries(self):
        self._make_mask(
            effective = now() + timedelta(days=3),
            expiration = now() + timedelta(days=30),
        )
        mask = get_active_mask()
        self.assertIsNone(mask)

    @patch('sitemask.masks._make_mask', autospec=True)
    def test_current_entry(self, make_mask_mock):
        make_mask_mock.return_value = sentinel.RESULT
        mask_record = self._make_mask(
            effective = now() - timedelta(days=3),
            expiration = now() + timedelta(days=3),
        )
        mask = get_active_mask()
        self.assertIs(mask, sentinel.RESULT)
        make_mask_mock.assert_called_once_with(mask_record)

    @patch('sitemask.masks._make_mask', autospec=True)
    def test_tied_entries(self, make_mask_mock):
        '''
        If two mask records are both "current," the one that most recently
        became effective is considered active.
        '''
        make_mask_mock.return_value = sentinel.RESULT
        older_mask_record = self._make_mask(
            effective = now() - timedelta(days=3),
            expiration = now() + timedelta(days=3),
        )
        newer_mask_record = self._make_mask(
            effective = now() - timedelta(days=1),
            expiration = now() + timedelta(days=3),
        )
        mask = get_active_mask()
        make_mask_mock.assert_called_once_with(newer_mask_record)

    @patch('sitemask.masks._make_mask', autospec=True)
    def test_very_tied_entries(self, make_mask_mock):
        '''
        If two mask records are both current, and both have the same effective
        date, the one that will expire first is considered active.
        '''
        make_mask_mock.return_value = sentinel.RESULT
        later_mask_record = self._make_mask(
            effective = now() - timedelta(days=3),
            expiration = now() + timedelta(days=5),
        )
        sooner_mask_record = self._make_mask(
            effective = now() - timedelta(days=3),
            expiration = now() + timedelta(days=3),
        )
        mask = get_active_mask()
        make_mask_mock.assert_called_once_with(sooner_mask_record)

    def test_tie_constraint(self):
        '''
        Two mask records can't tie for both effective and expiration dates,
        because the database won't allow it.
        '''
        effective = now() - timedelta(days=3)
        expiration = now() + timedelta(days=3)
        self._make_mask(effective=effective, expiration=expiration)
        with self.assertRaises(IntegrityError):
            self._make_mask(effective=effective, expiration=expiration)

    def _make_mask(self, **kwargs):
        defaults = {
            'title': 'Title',
            'subtitle': 'Subtitle',
            'image': '//test-image',
        }
        defaults.update(kwargs)
        return MaskModel.objects.create(**kwargs)


class MaskTransformTests(TestCase):
    def test_data_transform(self):
        title = 'Test Title'
        subtitle = 'Test Subtitle'
        image_url = '//test-image'
        effective = now() + timedelta(days=1)
        expiration = now() + timedelta(days=4)

        record = MaskModel.objects.create(
            title = title,
            subtitle = subtitle,
            image = image_url,
            effective = effective,
            expiration = expiration,
        )

        data = _make_mask(record)

        self.assertIsInstance(data, MaskData)
        self.assertEqual(data.title, title)
        self.assertEqual(data.subtitle, subtitle)
        self.assertEqual(data.image_url, image_url)

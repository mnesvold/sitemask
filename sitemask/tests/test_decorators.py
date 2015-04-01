from unittest.mock import create_autospec, Mock, patch, sentinel

from django.test import TestCase

from sitemask.decorators import maskable
from sitemask.masks import Mask

class SiteMaskDecoratorTests(TestCase):
    def setUp(self):
        self.get_active_mask_patch = patch(
            'sitemask.decorators.get_active_mask',
            autospec=True,
        )
        self.get_active_mask_mock = self.get_active_mask_patch.start()

    def tearDown(self):
        self.get_active_mask_patch.stop()

    def test_inactive(self):
        self.get_active_mask_mock.return_value = None
        view = Mock()
        decorated_view = maskable(view)

        args = (1, 2, 3)
        kwargs = {'foo': 'bar', 'bam': 'baz'}

        result = decorated_view(*args, **kwargs)

        self.get_active_mask_mock.assert_called_once_with()
        view.assert_called_once_with(*args, **kwargs)

    @patch('sitemask.decorators.render', autospec=True)
    def test_active(self, render_mock):
        title = sentinel.TITLE
        subtitle = sentinel.SUBTITLE
        image_url = sentinel.IMAGE_URL
        args = (sentinel.REQUEST, 1, 2, 3)
        kwargs = {'foo': 'bar', 'bam': 'baz'}

        active_mask = create_autospec(Mask, spec_set=True)
        active_mask.title = title
        active_mask.subtitle = subtitle
        active_mask.image_url = image_url

        render_mock.return_value = sentinel.RESPONSE
        self.get_active_mask_mock.return_value = active_mask
        view = Mock()
        decorated_view = maskable(view)

        result = decorated_view(*args, **kwargs)

        self.get_active_mask_mock.assert_called_once_with()
        self.assertFalse(view.called)
        self.assertIs(result, sentinel.RESPONSE)
        render_mock.assert_called_once_with(
            sentinel.REQUEST,
            'sitemask/mask.html',
            {
                'title': title,
                'subtitle': subtitle,
                'image_url': image_url,
            },
        )

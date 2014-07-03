from django.test import TestCase
from nose.tools import assert_equal
from sparkle.models import Application
from .models import macdown


class BaseTests(TestCase):
    """Tests for base module.
    """
    fixtures = ('sparkle.json',)

    def test_macdown(self):
        assert_equal(macdown, Application.objects.get(slug='macdown'))

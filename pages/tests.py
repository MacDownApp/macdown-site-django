import lxml.html
from lxml.cssselect import CSSSelector
from django.test import TestCase
from nose.tools import assert_equal, assert_not_equal
from sparkle.models import Version
from base.models import macdown


class PageTests(TestCase):
    """Tests for page loading.
    """
    fixtures = ('macdown', 'macdown_data')

    def _check_download_buttons(self, tree, version):
        """Check that download links in the tree are correct.

        There should be at least one download link, and all links should point
        to the version specified.
        """
        matches = CSSSelector('.download.button')(tree)
        assert_not_equal(len(matches), 0)
        for match in matches:
            assert_equal(match.get('href'), version.get_absolute_url())

    def test_home(self):
        latest_version = macdown.active_versions().latest()

        # Should load.
        response = self.client.get('/')
        assert_equal(response.status_code, 200)
        tree = lxml.html.fromstring(response.content)

        # Should contain download link in top navbar.
        for match in CSSSelector('.top-bar a')(tree):
            if match.get('href') == latest_version.get_absolute_url():
                break
        else:   # This happens if no matches are found
            self.fail('Download link not found in top navbar.')

        self._check_download_buttons(tree, latest_version)

    def test_features(self):
        latest_version = macdown.active_versions().latest()
        response = self.client.get('/features/')
        assert_equal(response.status_code, 200)
        tree = lxml.html.fromstring(response.content)
        self._check_download_buttons(tree, latest_version)

    def test_faq(self):
        latest_version = macdown.active_versions().latest()
        response = self.client.get('/faq/')
        assert_equal(response.status_code, 200)
        tree = lxml.html.fromstring(response.content)
        self._check_download_buttons(tree, latest_version)


class NoDownloadLinkTests(TestCase):
    """Test the download link if versions does not exist.
    """
    fixtures = ('macdown', 'macdown_data')

    def _test_home(self):
        # Should load.
        response = self.client.get('/')
        assert_equal(response.status_code, 200)
        tree = lxml.html.fromstring(response.content)

        # Should not contain download link in navbar.
        assert_equal(len(CSSSelector('.top-bar li.active a')(tree)), 0)

        # Should not contain download link.
        assert_equal(len(CSSSelector('.download.button')(tree)), 0)

    def test_no_default(self):
        # Remove versions from default channel.
        macdown.active_versions().delete()
        self._test_home()

    def test_nothing_at_all(self):
        # Remove all versions.
        Version.objects.all().delete()
        self._test_home()

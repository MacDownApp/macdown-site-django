from django.test import TestCase, Client
from nose.tools import assert_equal, assert_not_equal
from sparkle.models import Version


class DownloadTests(TestCase):
    """Tests for download link generation.
    """
    fixtures = ('macdown', 'macdown_data')

    def test_version_absolute_url(self):
        # Version with readable tag.
        version = Version.objects.get(short_version='0.1.2')
        assert_equal(version.get_absolute_url(), '/download/v0.1.2/')

        # Version without readable tag.
        version = Version.objects.get(version='217')
        assert_equal(version.get_absolute_url(), '/download/217/')

    def test_version(self):
        client = Client()

        # Resolve short version string.
        response = client.get('/download/v0.1.2/')
        assert_equal(response.status_code, 302)
        assert_equal(
            response['Location'],
            'https://github.com/MacDownApp/macdown/releases/download/v0.1.2/'
            'MacDown.app.zip',
        )

        # Resolve version number.
        response = client.get('/download/217/')
        assert_equal(response.status_code, 302)
        assert_equal(response['Location'], 'http://d.pr/f/3qn7+')

    def test_latest_version(self):
        client = Client()

        # Should point to the real lastest active version.
        response = client.get('/download/latest/')
        location = response['Location']
        assert_equal(response.status_code, 302)

        # Should not point to a newer, but non-active version.
        response = client.get('/download/v0.1.2/')
        assert_equal(location, response['Location'])
        response = client.get('/download/217/')
        assert_not_equal(location, response['Location'])

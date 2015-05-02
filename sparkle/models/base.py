from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


from ghostdown.models.fields import GhostdownField
from .compat import GenericIPAddressField
from .managers import VersionManager


@python_2_unicode_compatible
class Application(models.Model):
    """Representation of a Cocoa application."""

    name = models.CharField(
        max_length=50, verbose_name=_('name'),
    )
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name=_('slug'),
    )
    default_channel = models.ForeignKey(
        'Channel', verbose_name=_('default channel'), null=True,
    )

    class Meta:
        verbose_name = _('application')
        verbose_name_plural = _('applications')

    def __str__(self):
        return self.name

    def active_versions(self, channel=None):
        if channel is None:
            channel = self.default_channel
        return self.versions.active(channel=channel)


@python_2_unicode_compatible
class Channel(models.Model):
    """Possible channels in which a version belongs to."""

    name = models.CharField(
        max_length=50, verbose_name=_('name'),
    )
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name=_('slug'),
    )

    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('channels')

    def __str__(self):
        return self.name

    def active_versions(self, application):
        return application.active_versions(channel=self)


@python_2_unicode_compatible
class Version(models.Model):
    """A version for a given application."""

    application = models.ForeignKey(
        'Application', related_name='versions', verbose_name=_('application'),
    )
    channels = models.ManyToManyField(
        'Channel', related_name='versions', verbose_name=_('channels'),
    )
    title = models.CharField(
        max_length=100, verbose_name=_('title'),
    )
    version = models.CharField(
        max_length=10, verbose_name=_('version'),
        help_text=(
            'If you use short_version, this can be the internal version '
            'number or build number that will not be shown. In any case, this '
            'string is compared to CFBundleVersion of your bundle.'
        ),
    )
    short_version = models.CharField(
        max_length=50, blank=True, verbose_name=_('short version'),
        help_text='A user-displayable version string.',
    )
    dsa_signature = models.CharField(
        max_length=80, verbose_name=_('DSA signature'),
    )
    length = models.CharField(
        max_length=20, verbose_name=_('length'),
    )
    release_notes = GhostdownField(
        blank=True, verbose_name=_('release notes'),
    )
    minimum_system_version = models.CharField(
        max_length=10, verbose_name=_('minimum system version'),
    )
    update_url = models.URLField(
        max_length=200, verbose_name=_('update URL'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'),
    )
    publish_at = models.DateTimeField(
        default=now, verbose_name=_('published at'),
        help_text=('When this upate will be (automatically) published.'),
    )

    objects = VersionManager()

    class Meta:
        verbose_name = _('version')
        verbose_name_plural = _('versions')
        ordering = ('-publish_at',)
        get_latest_by = 'version'

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class SystemProfileReport(models.Model):
    """A system profile report."""

    ip_address = GenericIPAddressField(
        verbose_name=_('IP address'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'),
    )

    def __str__(self):
        return _('From {ip} at {t}').format(
            ip=self.ip_address, t=self.created_at
        )


@python_2_unicode_compatible
class SystemProfileReportRecord(models.Model):
    """A key-value pair for a system profile report."""

    report = models.ForeignKey(
        'SystemProfileReport', verbose_name=_('report'),
    )
    key = models.CharField(
        max_length=100, verbose_name=_('key'),
    )
    value = models.CharField(
        max_length=80, verbose_name=_('value'),
    )

    def __str__(self):
        return '{key}:{value}'.format(key=self.key, value=self.value)

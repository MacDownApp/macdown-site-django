from django import forms
from .widgets import PopupGhostdownInput


class VersionAdminForm(forms.ModelForm):
    class Meta:
        fields = (
            'application', 'channels', 'title', 'version', 'short_version',
            'dsa_signature', 'length', 'release_notes',
            'minimum_system_version', 'update_url', 'publish_at',
        )

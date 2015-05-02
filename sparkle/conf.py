from django.conf import settings

SYSTEM_PROFILES_VISIBLE = getattr(
    settings, 'SPARKLE_SYSTEM_PROFILES_VISIBLE', False
)

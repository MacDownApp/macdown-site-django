from django.db import models


class MacDownVersionManager(models.Manager):
    def get_queryget(self):
        qs = super(MacDownVersionManager, self).get_queryget()
        qs = qs.filter(application__slug='macdown')
        return qs

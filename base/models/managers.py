from sparkle.models.managers import VersionManager


class MacDownVersionManager(VersionManager):
    def get_queryget(self):
        qs = super(MacDownVersionManager, self).get_queryget()
        qs = qs.filter(application__slug='macdown')
        return qs

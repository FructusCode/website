from django.contrib.auth.models import User
from django.db import models
from website.apwan.core.database import unique_slugify
from website.apwan.models.service import Service

__author__ = 'Dean Gardiner'


class Payee(models.Model):
    class Meta:
        app_label = 'apwan'

    owner = models.ForeignKey(User)

    user = models.ForeignKey(Service, null=True)

    account_name = models.CharField(max_length=64, null=True, blank=True)
    account_id = models.IntegerField(null=True, blank=True)

    title = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32)

    def path(self):
        return '/account/payee/' + self.slug

    def save(self, **kwargs):
        unique_slugify(
            self, self.title,
            queryset=Payee.objects.all().filter(owner=self.owner)
        )
        super(Payee, self).save(kwargs)

    def dict(self):
        item = {
            'title': self.title,
            'slug': self.slug,
            'account_id': self.account_id,
            'account_name': self.account_name
        }

        if self.user:
            # pylint: disable=E1101
            item['user'] = self.user.dict()
            # pylint: enable=E1101
        else:
            item['user'] = None

        return item

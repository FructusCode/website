from django.contrib.auth.models import User
from django.db import models
from website.apwan.helpers.database import unique_slugify

__author__ = 'Dean Gardiner'


class Payee(models.Model):
    class Meta:
        app_label = 'apwan'
        unique_together = ('type', 'token')

    TYPE_WEPAY = 0

    TYPES = (
        (TYPE_WEPAY, "WePay"),
    )

    owner = models.ForeignKey(User)
    type = models.IntegerField(choices=TYPES)

    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32)

    account_id = models.IntegerField(unique=True, null=True)
    token = models.CharField(max_length=70, null=True)  # OAuth account authorization token

    def path(self):
        return '/account/payee/' + self.slug

    def save(self, **kwargs):
        unique_slugify(
            self, self.name,
            queryset=Payee.objects.all().filter(owner=self.owner)
        )
        super(Payee, self).save(kwargs)

    # returns a safe dict of the object (excluding the token)
    def dict(self):
        return {
            'name': self.name,
            'slug': self.slug,
            'type': self.type,
            'get_type_display': self.get_type_display()
        }
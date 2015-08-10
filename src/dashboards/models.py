# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from categories.models import Category
from dashboards.fields import DashboardProviderChoiceField


class Dashboard(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=50)
    slug = models.SlugField(
        _('Slug'),
        unique=True,
        db_index=True,
        max_length=250)
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'))
    data_provider = DashboardProviderChoiceField(
        _('Dashboard data provider'))

    class Meta:
        verbose_name = _('Dashboard')
        verbose_name_plural = _('Dashboard provider')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('dashboard_detail', args=[
            self.category.organisation.slug,
            self.slug
        ])
        return url

    @property
    def data_strategy(self):
        if not hasattr(self, '_data_strategy'):
            self._data_strategy = self.data_provider(category=self.category)
        return self._data_strategy

    def fetch_data(self):
        self.data_strategy.fetch_data()

    def get_headers(self):
        return self.data_strategy.get_headers()

    def get_buckets(self):
        self._data_strategy = self._data_strategy or self.data_provider()
        return self.data_strategy.get_buckets()

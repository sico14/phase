# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.forms import ModelChoiceField
from django.db import models

from elasticsearch_dsl import Search

from documents.forms.filters import filterform_factory
from search import elastic


class SearchBuilder(object):
    """Builds Elasticsearch query objects.

    Given a category and a dictionary of filters (as generated by the
    document list form filter, builds a search query using the python
    ES api.

    """

    def __init__(self, category, filters={}):
        self.category = category
        self.set_filters(filters)

        DocumentModel = self.category.document_class()
        Config = DocumentModel.PhaseConfig
        self.filter_fields = Config.filter_fields
        self.custom_filters = getattr(Config, 'custom_filters', {})
        self.searchable_fields = Config.searchable_fields

    def set_filters(self, filters):
        DocumentModel = self.category.document_class()
        FilterForm = filterform_factory(DocumentModel)
        form = FilterForm(filters)
        if not form.is_valid():
            raise RuntimeError('Search filters are invalid')

        self.filter_form = form
        self.filters = form.cleaned_data

    def get_results(self):
        return self.build_query().execute()

    def build_query(self):
        document_type = self.category.document_type()

        s = Search(using=elastic, doc_type=document_type) \
            .index(settings.ELASTIC_INDEX) \
            .filter('term', is_latest_revision=True)

        s = self._add_filter_fields(s)
        s = self._add_custom_filters(s)
        s = self._add_aggregations(s)
        s = self._add_search_query(s)
        s = self._add_sort(s)
        s = self._add_pagination(s)

        return s

    def _add_filter_fields(self, s):
        for field in self.filter_fields:
            value = self.filters.get(field, None)
            if value:
                if isinstance(value, models.Model):
                    value = value.pk
                    field = '%s_id' % field
                else:
                    field = '%s.raw' % field
                s = s.filter({'term': {field: value}})

        return s

    def _add_custom_filters(self, s):
        for filter_key, filter_data in self.custom_filters.items():
            value = self.filters.get(filter_key, None)
            f = filter_data['filters'].get(value, None)
            if f is not None:
                s = s.filter(f)

        return s

    def _add_aggregations(self, s):
        """Add aggregations (facets) to the search query.

        For foreign key fields, we need to organize buckets by primary keys
        For every other field, the ".raw" field is what we want

        """
        for field in self.filter_fields:
            if isinstance(self.filter_form.fields[field], ModelChoiceField):
                s.aggs.bucket(field, 'terms', field='%s_id' % field, size=0)
            else:
                s.aggs.bucket(field, 'terms', field='%s.raw' % field, size=0)

        return s

    def _add_search_query(self, s):
        """Add the full text search to the query."""
        search_terms = self.filters.get('search_terms', None)
        raw_search_fields = map(lambda x: '%s.raw' % x, self.searchable_fields)
        if search_terms:
            s = s.query({
                'multi_match': {
                    'query': search_terms,
                    'fields': ['_all'] + raw_search_fields,
                    'operator': 'and'
                }
            })

        return s

    def _add_sort(self, s):
        sort_field = self.filters.get('sort_by', 'document_key') or 'document_key'
        sort_field = '%s.raw' % sort_field
        if sort_field.startswith('-'):
            sort_field = sort_field.lstrip('-')
            sort_direction = 'desc'
        else:
            sort_direction = 'asc'
        s = s.sort({sort_field: {'order': sort_direction}})
        return s

    def _add_pagination(self, s):
        s = s.extra(
            from_=self.filters.get('start', 0),
            size=self.filters.get('size', settings.PAGINATE_BY)
        )
        return s

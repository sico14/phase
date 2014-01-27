from django.conf.urls import patterns, url

from documents.views import (
    DocumentList, DocumentFilter, DocumentCreate, DocumentDetail,
    DocumentEdit, DocumentDownload, DocumentRedirect, DocumentRevise,
    ProtectedDownload
)

urlpatterns = patterns(
    '',

    # Document short url
    url(r'^documents/(?P<document_key>[\w-]+)/$',
        DocumentRedirect.as_view(),
        name='document_short_url'),

    # Filters
    url(r'^(?P<organisation>[\w-]+)/(?P<category>[\w-]+)/filter/$',
        DocumentFilter.as_view(),
        name="document_filter"),

    # Downloads
    url(r'^(?P<organisation>[\w-]+)/(?P<category>[\w-]+)/download/$',
        DocumentDownload.as_view(),
        name="document_download"),
    url(r'^files/(?P<file_name>[-\w.]+)/$',
        ProtectedDownload.as_view(),
        name="protected_download"),

    # Documents
    url(r'^(?P<organisation>[\w-]+)/(?P<category>[\w-]+)/$',
        DocumentList.as_view(),
        name="category_document_list"),
    url(r'^(?P<organisation>[\w-]+)/(?P<category>[\w-]+)/create/$',
        DocumentCreate.as_view(),
        name="document_create"),
    url(r'^(?P<organisation>[\w-]+)/(?P<category>[\w-]+)/(?P<document_key>[\w-]+)/$',
        DocumentDetail.as_view(),
        name="document_detail"),
    url(r'^(?P<organisation>[\w-]+)/(?P<category>[\w-]+)/(?P<document_key>[\w-]+)/edit/$',
        DocumentEdit.as_view(),
        name="document_edit"),
    url(r'^(?P<organisation>[\w-]+)/(?P<category>[\w-]+)/(?P<document_key>[\w-]+)/revise/$',
        DocumentRevise.as_view(),
        name="document_revise"),
    url(r'^(?P<organisation>[\w-]+)/(?P<category>[\w-]+)/(?P<document_key>[\w-]+)/edit/(?P<revision>\d+)/$',
        DocumentEdit.as_view(),
        name="document_edit"),
)

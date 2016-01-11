# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from documents.forms.utils import DocumentDownloadForm
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Field

from default_documents.layout import DocumentFieldset, DateField

from documents.forms.models import GenericBaseDocumentForm
from reviews.forms import ReviewFormMixin
from transmittals.layout import RelatedRevisionsLayout, OutgoingTrsLayout
from transmittals.models import (
    Transmittal, TransmittalRevision, OutgoingTransmittal,
    OutgoingTransmittalRevision)


class TransmittalForm(GenericBaseDocumentForm):
    def build_layout(self):
        return Layout(
            Field('tobechecked_dir', type='hidden'),
            Field('accepted_dir', type='hidden'),
            Field('rejected_dir', type='hidden'),
            DocumentFieldset(
                _('General information'),
                Field('document_key', type='hidden'),
                'document_number',
                DateField('transmittal_date'),
                DateField('ack_of_receipt_date'),
                'contract_number',
                'originator',
                'recipient',
                'sequential_number',
                self.get_related_documents_layout(),
            )
        )

    class Meta:
        model = Transmittal
        exclude = ('document', 'latest_revision', 'status',
                   'transmittal_key', 'document_type', 'contractor',)


class TransmittalRevisionForm(GenericBaseDocumentForm):
    def build_layout(self):
        fields = (
            _('Revision'),
            DateField('revision_date'),
            DateField('received_date'),
            Field('created_on', readonly='readonly'))

        # native / pdf will be autogenerated
        if self.read_only:
            fields += (
                'native_file',
                'pdf_file')

        return Layout(DocumentFieldset(*fields))

    class Meta:
        model = TransmittalRevision
        exclude = ('document', 'revision', 'trs_status', 'updated_on')


class OutgoingTransmittalForm(GenericBaseDocumentForm):
    def get_related_documents_layout(self):
        related_documents = DocumentFieldset(
            _('Related documents'),
            RelatedRevisionsLayout('related_documents'))
        return related_documents

    def build_layout(self):
        return Layout(
            DocumentFieldset(
                _('General information'),
                Field('document_key', type='hidden'),
                'document_number',
                'contract_number',
                'originator',
                'recipient',
                'sequential_number',
                DateField('ack_of_receipt_date'),
                self.get_related_documents_layout(),
            )
        )

    class Meta:
        model = OutgoingTransmittal
        exclude = ('document', 'latest_revision',
                   'related_documents')


class OutgoingTransmittalRevisionForm(GenericBaseDocumentForm):
    def build_layout(self):
        fields = (
            _('Revision'),
            DateField('revision_date'),
            DateField('received_date'),
            Field('created_on', readonly='readonly'))

        # native / pdf will be autogenerated
        if self.read_only:
            fields += ('pdf_file',)

        return Layout(DocumentFieldset(*fields))

    class Meta:
        model = OutgoingTransmittalRevision
        exclude = ('document', 'revision', 'updated_on')


class TransmittalDownloadForm(DocumentDownloadForm):
    content = forms.ChoiceField(
        choices=(
            ('transmittal', "Transmittal"),
            ('revisions', "Revisions"),
            ('both', "Both"),
        ),
        required=False)


class TransmittableFormMixin(ReviewFormMixin):

    def get_trs_layout(self):
        if self.read_only:
            layout = (DocumentFieldset(
                _('Outgoing Transmittal'),
                OutgoingTrsLayout('transmittal'),
            ),)
        else:
            layout = tuple()
        return layout

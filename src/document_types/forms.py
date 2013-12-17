from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from documents.forms.models import BaseDocumentForm
from .models import ContractorDeliverable
from .layout import (
    ScheduleLayout, ScheduleStatusLayout, FlatRelatedDocumentsLayout)


class ContractorDeliverableForm(BaseDocumentForm):
    def __init__(self, *args, **kwargs):
        super(ContractorDeliverableForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = self.build_layout()

    def build_layout(self):
        if self.read_only:
            related_documents = Fieldset(
                _('Related documents'),
                FlatRelatedDocumentsLayout('related_documents'),
            )
        else:
            related_documents = Fieldset(
                _('Related documents'),
                'related_documents',
            )

        return Layout(
            Fieldset(
                _('General information'),
                'document_key',
                'title',
                'contract_number',
                'originator',
                'unit',
                'discipline',
                'document_type',
                'sequential_number',
                'project_phase',
                'klass',
                'system',
                'wbs',
                'weight',

            ),
            related_documents,
            Fieldset(
                _('Schedule'),
                ScheduleLayout(
                    ScheduleStatusLayout('std'),
                    ScheduleStatusLayout('idc'),
                    ScheduleStatusLayout('ifr'),
                    ScheduleStatusLayout('ifa'),
                    ScheduleStatusLayout('ifd'),
                    ScheduleStatusLayout('ifc'),
                    ScheduleStatusLayout('ifi'),
                    ScheduleStatusLayout('asb'),
                )
            )
        )

    class Meta:
        model = ContractorDeliverable
        exclude = ('document', 'latest_revision')
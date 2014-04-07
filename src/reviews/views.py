from django.views.generic import ListView
from django.db.models import Q

from accounts.views import LoginRequiredMixin
from documents.utils import get_all_revision_classes
from reviews.models import ReviewMixin


class DocumentList(LoginRequiredMixin, ListView):
    template_name = 'reviews/document_list.html'
    context_object_name = 'revisions'

    def get_context_data(self, **kwargs):
        context = super(DocumentList, self).get_context_data(**kwargs)
        context.update({
            'reviews_active': True,
        })
        return context

    def get_queryset(self):
        """Get all documents under review.

        Since documents can be of differente types, we need to launch a query
        for every document type that is reviewable.  We assume that the number
        of reviewable document classes will never be too high, so we don't do
        anything to optimize performances for now.

        """
        user = self.request.user
        q_reviewers = Q(reviewers=user)
        q_approver = Q(approver=user)
        q_leader = Q(leader=user)

        revisions = []
        klasses = [klass for klass in get_all_revision_classes() if issubclass(klass, ReviewMixin)]

        for klass in klasses:
            qs = klass.objects \
                .filter(q_reviewers | q_approver | q_leader) \
                .select_related('document')
            revisions += list(qs)

        return revisions

from django_elasticsearch_dsl_drf_alt.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf_alt.viewsets import DocumentViewSet

from ..documents import TagDocument
from ..serializers import TagDocumentSerializer

__all__ = ("TagDocumentViewSet",)


class TagDocumentViewSet(DocumentViewSet):
    """Document viewset for tags."""

    document = TagDocument
    serializer_class = TagDocumentSerializer
    lookup_field = "title"
    filter_backends = []
    pagination_class = LimitOffsetPagination

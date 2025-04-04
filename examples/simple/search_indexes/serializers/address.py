from django_elasticsearch_dsl_drf_alt.serializers import DocumentSerializer

from ..documents import AddressDocument

__all__ = (
    "AddressDocumentSerializer",
    "FrontendAddressDocumentSerializer",
)


class AddressDocumentSerializer(DocumentSerializer):
    """Serializer for address document."""

    class Meta:
        """Meta options."""

        document = AddressDocument
        fields = (
            "id",
            "street",
            "house_number",
            "appendix",
            "zip_code",
            "city",
            "country",
            "continent",
            "location",
        )


class FrontendAddressDocumentSerializer(DocumentSerializer):
    """Serializer for address document."""

    class Meta:
        """Meta options."""

        document = AddressDocument
        fields = (
            "id",
            "street",
            "house_number",
            "appendix",
            "zip_code",
            "location",
        )

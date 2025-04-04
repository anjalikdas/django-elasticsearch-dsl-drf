from django.conf import settings

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf_alt.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf_alt.versions import ELASTICSEARCH_GTE_5_0

from books.models import Address

from .analyzers import html_strip


__all__ = ("AddressDocument",)

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={"read_only_allow_delete": False},
    # read_only_allow_delete=False
)


@INDEX.doc_type
class AddressDocument(Document):
    """Address Elasticsearch document."""

    # In different parts of the code different fields are used. There are
    # a couple of use cases: (1) more-like-this functionality, where `title`,
    # `description` and `summary` fields are used, (2) search and filtering
    # functionality where all of the fields are used.

    # ID
    id = fields.IntegerField(attr="id")

    # ********************************************************************
    # *********************** Main data fields for search ****************
    # ********************************************************************
    __street_fields = {
        "raw": KeywordField(),
        "suggest": fields.CompletionField(),
    }

    if ELASTICSEARCH_GTE_5_0:
        __street_fields.update(
            {
                "suggest_context": fields.CompletionField(
                    contexts=[
                        {
                            "name": "loc",
                            "type": "geo",
                            "path": "location",
                            "precision": "1000km",
                        },
                    ]
                ),
            }
        )
    street = StringField(analyzer=html_strip, fields=__street_fields)

    house_number = StringField(analyzer=html_strip)

    appendix = StringField(analyzer=html_strip)

    zip_code = StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
        },
    )

    # ********************************************************************
    # ********** Additional fields for search and filtering **************
    # ********************************************************************

    # City object
    city = fields.ObjectField(
        properties={
            "name": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
            "info": StringField(analyzer=html_strip),
            "location": fields.GeoPointField(attr="location_field_indexing"),
            "country": fields.ObjectField(
                properties={
                    "name": StringField(
                        analyzer=html_strip,
                        fields={
                            "raw": KeywordField(),
                            "suggest": fields.CompletionField(),
                        },
                    ),
                    "info": StringField(analyzer=html_strip),
                    "location": fields.GeoPointField(attr="location_field_indexing"),
                }
            ),
        }
    )

    # Country object
    country = fields.NestedField(
        attr="country_indexing",
        properties={
            "name": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
            "city": fields.ObjectField(
                properties={
                    "name": StringField(
                        analyzer=html_strip,
                        fields={
                            "raw": KeywordField(),
                        },
                    ),
                },
            ),
        },
    )

    # Continent object
    continent = fields.NestedField(
        attr="continent_indexing",
        properties={
            "id": fields.IntegerField(),
            "name": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
            "country": fields.NestedField(
                properties={
                    "id": fields.IntegerField(),
                    "name": StringField(
                        analyzer=html_strip,
                        fields={
                            "raw": KeywordField(),
                        },
                    ),
                    "city": fields.NestedField(
                        properties={
                            "id": fields.IntegerField(),
                            "name": StringField(
                                analyzer=html_strip,
                                fields={
                                    "raw": KeywordField(),
                                },
                            ),
                        }
                    ),
                }
            ),
        },
    )

    # Galaxy object
    galaxy = fields.ObjectField(
        attr="galaxy_indexing",
        properties={
            "id": fields.IntegerField(),
            "name": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                    "suggest": fields.CompletionField(),
                },
            ),
            "planet": fields.NestedField(
                properties={
                    "id": fields.IntegerField(),
                    "name": StringField(
                        analyzer=html_strip,
                        fields={
                            "raw": KeywordField(),
                        },
                    ),
                }
            ),
        },
    )

    location = fields.GeoPointField(
        attr="location_field_indexing",
    )

    class Django(object):
        model = Address  # The model associate with this Document

    class Meta:
        parallel_indexing = True
        # queryset_pagination = 500000  # This will split the queryset
        #                               # into parts while indexing

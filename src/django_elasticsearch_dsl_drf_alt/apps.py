"""
Apps.
"""

from django.apps import AppConfig

__title__ = "django_elasticsearch_dsl_drf_alt.apps"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2017-2020 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("Config",)


class Config(AppConfig):
    """Config."""

    name = "django_elasticsearch_dsl_drf_alt"
    label = "django_elasticsearch_dsl_drf_alt"

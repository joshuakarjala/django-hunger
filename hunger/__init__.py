"""
Hunger is a Django app to manage a private beta phase.
"""
import pkg_resources

__version__ = pkg_resources.get_distribution('django_hunger').version

VERSION = __version__

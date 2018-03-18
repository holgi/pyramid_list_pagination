'''Pyramid List Pagination contains helpers for pagination of result lists.

The package provides three classes to ease the creation of paginated result
lists:

* ``Pagination``: calculate pagination info, like first page, last page, etc.
* ``SQLAlchemyListing``: create paginated results with custom ordering
* ``ListingResource``: location aware resource for result lists


Features
--------

* automatically calculate pagination information like first, next or last page
  from `pyradmid.request.GET` parameters
* loading configuration defaults from .ini files
* easily implement ordering and filtering of results
* helper method for creating `pyradmid.request.GET` parameters for different
  pages
* base class for listings as location aware pyramid resources
'''


__author__ = 'Holger Frey'
__email__ = 'mail@holgerfrey.de'
__version__ = '0.1.8'


from .listing import SQLAlchemyListing  # noqa: F401
from .pagination import Pagination, includeme  # noqa: F401
from .resource import ListingResource  # noqa: F401

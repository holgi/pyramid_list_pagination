'''Top-level package for Pyramid List Pagination.'''

__author__ = 'Holger Frey'
__email__ = 'mail@holgerfrey.de'
__version__ = '0.1.2'


from .listing import SQLAlchemyListing
from .pagination import Pagination, includeme
from .resource import ListingResource

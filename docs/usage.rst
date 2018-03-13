=====
Usage
=====

To use Pyramid List Pagination in a pyramid project with configuration loaded
from an .ini file add this line to your main() function::

    config.include('pyramid_listing')

and later when defining custom result lists::

    import pyramid_listing


For an example implementation take a look at
https://github.com/holgi/pyramid_listing_example


Pagination
----------

.. automodule:: pyramid_listing.pagination


Result Lists
------------

.. automodule:: pyramid_listing.listing


Result Lists as Resources
-------------------------

.. automodule:: pyramid_listing.resource

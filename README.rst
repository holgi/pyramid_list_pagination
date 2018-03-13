=======================
Pyramid List Pagination
=======================

Pyramid List Pagination contains pyramid resources and helpers for pagination
of result lists.

A lot of pyramid_ applications that use a (SQL) database need to list the result
of queries. This result list might get quite long and are split into several
pages. This package is offering some help in this.


Quickstart
----------

Lets assume, that you'd like to start a cheese shop and define a simple
database model in the pyramid application::

    from .meta import Base

    class Cheese(Base):
        id = Column(Integer, primary_key=True)
        name = Column(Text, nullable=False)

To get a result list including pagination, just create a sub-class from
:class:`pyramid_listing.SQLAlchemyListing` and define a ``get_base_query``
method::

    from pyramid_listing import SQLAlchemyListing

    class CheeseList(SQLAlchemyListing):

        def get_base_query(self, request)
            return request.dbsession.query(Cheese)

In a view you could then use this class to autmagically get paged results::

    @view_config(route_name='cheeses')
    def cheese_list_view(request):
        listing = CheeseList(request)
        return {'cheeses': listing.items(), 'pagination': listing.pages}

With this URLs you could access different result pages:

    shows page 3:

    https://example.com/cheeses?p=3

    shows page 1 with 42 items per page:

    https://example.com/cheeses?p=1&n=42


Features
--------

* automatically calculate pagination information like first, next or last page
  from `pyradmid.request.GET` parameters
* loading configuration defaults from .ini files
* easily implement ordering and filtering of results
* helper method for creating `pyradmid.request.GET` parameters for different
  pages
* base class for listings as location aware pyramid resources


Example Project
---------------

To see this in action install the sample project from
https://github.com/holgi/pyramid_listing_example
and take a look at it


Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _pyramid: https://trypyramid.com

''' The ``pyramid_listing.resources`` modules provides a base class
for simple (SQLAlchemy) results list as location aware pyramid resources.

One of the my most beloved features of the pyramid framework are Ressources_,
especially since they enable traversal style routing and simple access controll
lists.

The :class:`ListingResource` base class provided by this module extends the
:class:`pyramid_listing.listing.SQLAlchemyListing` class. To define a result
list as a resource, you subclass from :class:`ListingResource`, provide a
``get_base_query()`` method (required by SQLAlchemyListing) and a
``resource_from_model()`` method::

    class DummyCheeseResource:

        def __init__(self, model):
            self.model = model


    class SimplestCheeseListResource(ListingResource):

        def base_query(self, request):
            return request.dbsession.query(Cheese)

        def resource_from_model(self, model):
            return DummyCheeseResource(model)

Instead of returning a list of pure database models when calling the
``items()`` method, the result in this case will be a list of
``DummyCheeseResources``.

If you define a ``__getitem__`` method and provide location aware model
resources, you'd have a resource tree for traversal style routing with
pagination, ordering, etc::


    class CheeseResource:

        def __init__(self, model, parent):
            self.model = model
            self.__name__ == model.id
            self.__parent__ == parent


    class CheeseListResource(ListingResource):

        def base_query(self, request):
            return request.dbsession.query(Cheese)

        def resource_from_model(self, model):
            return CheeseResource(model, self)

.. _Ressources: https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html
'''

from .listing import SQLAlchemyListing
from .pagination import Pagination


class ListingResource(SQLAlchemyListing):
    ''' sql helper for result lists as location aware resources

    This base class can help to produce paginated results from SQLAlchemy
    queries as location aware resouces for traversal style routing in pyramid
    apps.

    Derived classes
        - *must* implement the :func:`__getitem__()` method
        - *must* implement the :func:`resource_from_model()` method
        - *must* implement the :func:`set_base_query()` method
          from SQLAlchemyListing
        - *should* provide a :func:`get_order_by_field()` method
          from SQLAlchemyListing
        - *may* make use of the :func:`set_filtered_query()` method
          from SQLAlchemyListing

    If you implement ordering of the results with the
    :func:`get_order_by_field()` method, it is highly recommended to set the
    `default_order_by_field` and `default_order_by_direction` properties.

    An example::

        from pyramid_listing import ListingResource

        # import the relevant SQLAlchemy model
        from models import Cheeses


        class CheeseResource:

            def __init__(self, model, parent):
                self.model = model
                self.__name__ = model.id
                self.__parent__ = parent


        class CheeseListResource(ListingResource):

            def __init__(self, request, name=None, parent=None):
                super().__init__(request, name=None, parent=None)
                self.default_order_by_field = 'name'
                self.default_order_by_direction = 'asc'

            def __getitem__(self, key):
                model = self.base_query.get(key)
                if model:
                    return self.resource_from_model(model)
                raise KeyError

            def resource_from_model(self, model):
                return CheeseResource(model, parent=self)


            # the following methods are defined in the ListingResource class

            def get_base_query(self, request):
                # show only in-stock items
                return (
                    request.dbsession
                    .query(Cheeses)
                    .filter_by(in_stock==True)
                    )

            def get_filtered_query(self, base_query, request):
                query = base_query
                # filter by type of cheese
                cheese_type = request.GET.get('type', None)
                if cheese_type is not None:
                    query = query.filter_by(database_model_field=cheese_type)
                    # remember this filter for other urls
                    self.remember('type', cheese_type)
                return query

            def get_order_by_field(self, order_by):
                if order_by.lower() == 'name':
                    return Cheeses.name
                if order_by.lower() == 'manufacturer':
                    return Cheeses.manufacturer
                if order_by.lower() == 'price':
                    return Cheeses.price_per_kilo
                return None


        @view_config(context=CheeseListResource)
        def view_cheeses_in_stock(request):
            return {'cheeses': listing.items()}

    In this example, the following urls will show you different pages, etc::

        # shows page 3
        request.resource_url(context, query=context(p=3))

        # shows page 3, ordered by descending price
        request.route_url(context, query=context(p=3, o='price', d='desc'))

        # shows page 1 with 42 items per page
        request.route_url(context, query=context(p=1, n=42))

        # shows page 2 of blue cheeses
        request.route_url(context, query=context(p=2, type='blue'))


    :param pyramid.Request request: request object
    :param pagination_class: class of the pagination calculator to use
    :param str name: name of the resource for location awareness
    :param parent: parent resource for location awareness

    :ivar str __name__: key to retrive this location aware resource from parent
    :ivar __parent__: parent resource of this location aware resource
    :ivar pyramid.Request request: the current request object
    :ivar pyramid_listing.Pagination pages: pagination information
    :ivar str default_order_by_field: default field to order the results by
    :ivar str default_order_by_direction: default direction to order results
    :ivar sqlalchemy.query base_query: basic database query
    :ivar sqlalchemy.query filtered_query: database query with custom filters
    '''

    def __init__(self,
                 request,
                 pagination_class=Pagination,
                 name=None,
                 parent=None
                 ):
        ''' Instance creation

        :param pyramid.Request request: request object
        :param str name: name of the resource for location awareness
        :param parent: parent resource for location awareness
        :param pagination_class: class of the pagination calculator to use
        '''
        self.__name__ = name
        self.__parent__ = parent
        super().__init__(request, pagination_class)

    def items(self):
        ''' returns a iterable of child resources for the page '''
        return [self.resource_from_model(item) for item in super().items()]

    def __getitem__(self, key):
        ''' returns a single child resource from a model identified by key

        This is just the most simple implementation.
        '''
        model = self.base_query.get(key)
        if model:
            return self.resource_from_model(model)
        raise KeyError

    def resource_from_model(self, model):
        ''' returns a child resource from an sqlalchemy model instance '''
        raise NotImplementedError

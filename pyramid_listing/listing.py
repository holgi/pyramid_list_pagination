''' The ``pyramid_listing.listing`` modules provides a base class
for simple (SQLAlchemy) results list.

To define a result list, you inherit from :class:`SQLAlchemyListing` and
provide at least a ``get_base_query()`` method::

    class MostSimpleListing(SQLAlchemyListing):

        def get_base_query(self, request):
            return request.dbsession.query(Cheese)

The base query could also include a filter by method. Let's say the listing
should only contain published articles, the method would look like this::

    class OnlyPublishedArticles(SQLAlchemyListing):

        def get_base_query(self, request):
            return (
                request.dbsession
                .query(Article)
                .filter_by(published==True)
                )

This offers pagination via the :class:`pyramid_listing.pagination.Pagination`
class. The pagination information is exposed through the ``pages`` property::

    listing = MostSimpleListing(request)
    listing.pages.current == 1
    listing.pages.next == 2

If you want to provide filters via request.GET (e.g. a search functionality)
you need to define a custom ``get_filtered_query()`` method::

    class SearchableListing(SQLAlchemyListing):

        def get_base_query(self, request):
            return request.dbsession.query(Cheese)

        def get_filtered_query(self, base_query, request):
            search = request.GET.get('search')
            if search is not None:
                # remember this for creaing further query parameters
                self.remember('search', search)
                term = f'%{search}%'
                return base_query.filter(Cheese.name.ilike(term))
            else:
                return base_query

Paginatination information is calculated on the filtered query, so no need to
worry there.

Besides paginatinon and filtering the third most common thing to do is to
provide different ordering of the results, e.g. by name, country, date or
anything. Therfore you should provide a ``get_order_field()`` method. For a
nice ordering behaviour you should also set this two class properties:
``default_order_by_field`` and ``default_order_by_direction``::

    class OrderedListing(SQLAlchemyListing):

        default_order_by_field = 'name'
        default_order_by_direction = 'asc'

        def __init__(self, request):
            super().__init__(request)

        def get_base_query(self, request):
            return request.dbsession.query(Cheese)

        def get_order_by_field(self, identifier):
            map = {
                'name': Cheese.name
                'country': Cheese.country
                'type': Cheese.type
                }
            return map.get(identifier, None)

The most tedious thing about pagination and ordering is creating the right
query parameters for requests. Therfore the ``query_params()`` method is
exposed::

    assert request.GET['p'] == 2  # page number two
    assert request.GET['n'] == 10  # ten items per page
    assert request.GET['o'] == 'type'  # order by type
    assert request.GET['d'] == 'desc'  # descending order

    listing = OrderedListing(request)

    # without modifications
    listing.query_params() == {'p':2, 'n':10, 'o':'type', 'd':'desc'}

    # page no 1
    listing.query_params(p=1) == {'p':1, 'n':10, 'o':'type', 'd':'desc'}

    # default sorting
    listing.query_params(o=None, d=None) == {'p':2, 'n':10}

Instead of of using ``query_params``, the instance is a callable. So the three
parameters above could also be accessed by::

    # without modifications
    listing() == {'p':2, 'n':10, 'o':'type', 'd':'desc'}

    # page no 1
    listing(p=1) == {'p':1, 'n':10, 'o':'type', 'd':'desc'}

    # default sorting
    listing(o=None, d=None) == {'p':2, 'n':10}

'''

from .pagination import Pagination

try:
    from sqlalchemy import asc, desc
except ImportError:
    pass


class SQLAlchemyListing:
    ''' sql helper for result lists

    This base class can help to produce paginated results from SQLAlchemy
    queries.

    Derived classes
        - *must* implement the :func:`get_base_query()` method,
        - *should* provide a :func:`get_order_by_field()` method and
        - *may* make use of the :func:`get_filtered_query()` method.

    If you implement ordering of the results with the
    :func:`get_order_by_field()` method, it is highly recommended to set the
    `default_order_by_field` and `default_order_by_direction` class properties.

    An example::

        from pyramid_listing import SQLAlchemyListing

        # import the relevant SQLAlchemy model
        from models import Cheeses

        class CheeseList(SQLAlchemyListing):

            default_order_by_field = 'name'
            default_order_by_direction = 'asc'

            def __init__(self, request):
                super().__init__(request)

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

            def get_order_by_field(self, identifier):
                if identifier.lower() == 'name':
                    return Cheeses.name
                if identifier.lower() == 'manufacturer':
                    return Cheeses.manufacturer
                if identifier.lower() == 'price':
                    return Cheeses.price_per_kilo
                return None


        @view_config(route_name='cheese_list')
        def view_cheeses_in_stock(request):
            listing = CheeseList(request)
            return {'listing':listing, 'cheeses':listing.items()}

    In this example, the following urls will show you different pages, etc::

        # shows page 3
        request.route_url('cheese_list', _query=listing(p=3))

        # shows page 3, ordered by descending price
        request.route_url(
            'cheese_list',
            _query=listing(p=3, o='price', d='desc')
            )

        # shows page 1 with 42 items per page
        request.route_url('cheese_list', _query=listing(p=1, n=42))

        # shows page 2 of blue cheeses
        request.route_url(
            'cheese_list', _query=listing(p=2, type='blue')
            )

    :param pyramid.Request request: request object
    :param pagination_class: class of the pagination calculator to use

    :cvar str default_order_by_field: default field to order the results by
    :cvar str default_order_by_direction: default direction to order results

    :ivar pyramid.Request request: the current request object
    :ivar pyramid_listing.Pagination pages: pagination information
    :ivar sqlalchemy.query base_query: basic database query
    :ivar sqlalchemy.query filtered_query: database query with custom filters
    '''

    #: Request.GET key for the field to order the results
    request_key_order_by_field = 'o'

    #: Request.GET key for the direction to order the results
    request_key_order_by_direction = 'd'

    #: string identifier of the field to order by
    default_order_by_field = None

    #: default direction to order by, either 'asc' or 'desc'
    default_order_by_direction = None

    def __init__(self, request, pagination_class=Pagination):
        ''' sql helper for result lists

        :param pyramid.Request request: request object
        :param pagination_class: class of the pagination calculator to use
        '''
        #: current pyramid.Request object
        self.request = request
        #: active order by field
        self.order_by = None
        #: active order by direction
        self.order_dir = None
        #: remember these request parameters for active filters
        self.filters = {}
        #: calculated pagination information
        self._pages = None
        #: basic database query
        self.base_query = self.get_base_query(request)
        #: database query with custom filters
        self.filtered_query = self.get_filtered_query(self.base_query, request)
        #: database query with custom filters and custom order
        self.ordered_query = self.get_ordered_query(
            self.filtered_query, request
            )

    def get_base_query(self, request):
        ''' setup of the basic database query

        :param pyramid.Request request: request object
        :returns: the basic sqlalchemy query for the listing

        The base query is used for basic filtering that should be applied in
        all cases; for example to filter out any products that are not in stock
        or ariticles in draft mode.

        This method must be implemented in a inherited class, an example::

            def set_base_query(self, request):
                return (
                    request.dbsession
                    .query(Cheeses)
                    .filter_by(in_stock==True)
                    )
        '''
        raise NotImplementedError

    def get_filtered_query(self, base_query, request):
        ''' setup of the database query for a specific view

        :param sqlalchemy.Query base_query: the basic query for the listing
        :param pyramid.Request request: request object
        :returns: sqlalchemy query with custom filters

        the filtered query extends the base query and applies filters for a
        specific view, like show only blue cheeses. This query is used for
        calulating pagination and sorting is applied when listing child
        resources.

        It is important to remember applied filters if they should be used for
        constructing other urls' query parameters.

        Here an example method that may be implemented in a inherited class::

            def get_filtered_query(self, base_query, request):
                query = base_query
                # filter by type of cheese
                cheese_type = request.GET.get('type', None)
                if cheese_type is not None:
                    query = query.filter_by(database_model_field=cheese_type)
                    # remember this filter for other urls
                    self.remember('type', cheese_type)
                return query

        '''
        return base_query

    def get_ordered_query(self, filtered_query, request):
        ''' applies a sorting to the filtered query and returns it

        :param sqlalchemy.Query filtered_query: query with custom filters
        :param pyramid.Request request: request object
        :returns: sqlalchemy query with ordering applied
        '''
        query = filtered_query

        # apply sorting from request.GET parameters
        order_param = self.request.GET.get(self.request_key_order_by_field)
        order_field = self.get_order_by_field(order_param)

        if order_field is not None:
            order_dir = self.request.GET.get(
                self.request_key_order_by_direction,
                'asc'
                )
            order_func = desc if order_dir.lower().startswith('d') else asc
            query = query.order_by(order_func(order_field))
            # remember the applied ordering for url query parameters
            self.order_by = order_param
            self.order_dir = 'asc' if order_func is asc else 'desc'

        # apply the default sorting if the current sorting field is other than
        # the default sorting
        default_field = self.get_order_by_field(self.default_order_by_field)
        if default_field is None:
            # no default order by field set, we can stop here
            return query

        if order_field is None or default_field != order_field:
            # apply default sorting only if the requested field is not the
            # default field
            direction = self.default_order_by_direction or 'asc'
            order_func = desc if direction.lower().startswith('d') else asc
            query = query.order_by(order_func(default_field))

        if order_field is None:
            # only remember default, if no ordering is set from request
            self.order_by = self.default_order_by_field
            self.order_dir = 'asc' if order_func is asc else 'desc'

        return query

    def get_order_by_field(self, identifier):
        ''' returns the SQLalchemy model field to sort by or None

        :param str identifier: a identifier for the field to sort by
        :returns: SQLalchemy model field or None

        This method should be implemented in a inherited class::

            def get_sort_by_field(self, identifier):
                if identifier == 'type':
                    return Cheese.type
                return None
        '''
        return None

    def items(self):
        ''' returns a list of database items for the current page '''
        if self.pages.items_total == 0:
            return []

        offset, limit = self.pages.offset, self.pages.limit
        query = self.ordered_query.offset(offset).limit(limit)
        return query.all()

    def __iter__(self):
        ''' returns an iterable of database items for the current page '''
        # The result of __iter__ must be an iterator,
        # returning a list directly is not suitable.
        return (item for item in self.items())

    @property
    def order_direction(self):
        return self.order_dir

    def remember(self, key, value):
        ''' remembers a key, value pair for constructing query parameters '''
        self.filters[key] = value

    def query_params(self, **kwargs):
        ''' returns query parameters for the active filters, ordering and page

        :param dict kwargs:
            values that override the current filter, ordering or page settings

        Example::

            listing = SQLAlchemyListing()
            # current page, sorting, etc.
            current = listing.query_params()
            current == {'p':1, 'n':12, 'o':'name', 'd':'asc', 'type':'brie'}
            # next page with same sorting but type filter removed
            next_ = listing.query_params({'p':2, 'type': None})
            next_ == {'p':2, 'n':12, 'o':'name', 'd':'asc'}

        Instead of using the query_params() method, you could also use
        the class as a callable::

            next_ = listing({'p':2, 'type': None})
            next_ == {'p':2, 'n':12, 'o':'name', 'd':'asc'}
        '''
        params = {
            self.pages.items_per_page_request_key: self.pages.items_per_page,
            self.pages.current_page_request_key: self.pages.current,
            self.request_key_order_by_field: self.order_by,
            self.request_key_order_by_direction: self.order_dir
            }
        params.update(self.filters)
        params.update(kwargs)
        return {k: v for k, v in params.items() if v is not None}

    def __call__(self, **kwargs):
        ''' returns query parameters for the active filters, ordering and page

        this is just a shorter version of SQLAlchemyListing.query_params()::

            listing = SQLAlchemyListing()
            # url for page number two with query_params()
            request.resource_url(self, query=listing.query_params(p=2))
            # url for page number two with __call__()
            request.resource_url(self, query=listing(p=2))
        '''
        return self.query_params(**kwargs)

    @property
    def pages(self, pagination_class=Pagination):
        ''' returns the pagination information

        :params pagination_class: class for calculating pagination information
        :raises NotImplementedError: if `self.filtered_query` is not set

        The first access of this property will trigger a query to get the
        total number of items of the filtered query without pagination.
        '''
        if self._pages is None:
            if not self.filtered_query:
                raise NotImplementedError('A filtered query is not set')
            items_total = self.filtered_query.count()
            self._pages = pagination_class(self.request, items_total)
        return self._pages

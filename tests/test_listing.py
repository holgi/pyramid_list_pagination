'''Tests for `pyramid_listing.listing` Listing class.'''

import pytest

from . import DummyRequest
from .database_fixture import Cheese, dbsession  # noqa: F401


@pytest.fixture
def test_class():
    from pyramid_listing.listing import SQLAlchemyListing

    class TestImplementation(SQLAlchemyListing):

        default_order_by_field = 'name'
        default_order_by_direction = 'asc'

        def __init__(self, request):
            super().__init__(request)

        def get_base_query(self, request):
            return request.dbsession.query(Cheese)

        def get_filtered_query(self, base_query, request):
            country = request.GET.get('country', None)
            if country:
                return base_query.filter_by(country=country)
            return base_query

        def get_order_by_field(self, order_by):
            map = {
                'country': Cheese.country,
                'name': Cheese.name,
                'region': Cheese.region
                }
            return map.get(order_by, None)

    return TestImplementation


def test_base_class_inititalization_raises_error():
    from pyramid_listing.listing import SQLAlchemyListing
    with pytest.raises(NotImplementedError):
        SQLAlchemyListing(DummyRequest())


def test_base_class_get_base_query_raises_error():
    from pyramid_listing.listing import SQLAlchemyListing
    with pytest.raises(NotImplementedError):
        SQLAlchemyListing.get_base_query(None, None)


def test_base_class_filtered_query_returns_base_query():
    from pyramid_listing.listing import SQLAlchemyListing
    result = SQLAlchemyListing.get_filtered_query(None, 'Something', None)
    assert result == 'Something'


def test_base_class_get_order_by_field():
    from pyramid_listing.listing import SQLAlchemyListing
    result = SQLAlchemyListing.get_order_by_field(None, 'Something')
    assert result is None


def test_implementation_inititalization(dbsession, test_class):  # noqa: F811
    from sqlalchemy.orm.query import Query
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    assert instance.request == request
    assert isinstance(instance.base_query, Query)
    assert instance.base_query == instance.filtered_query


def test_implementation_items_no_results_shortcut(  # noqa: F811
        dbsession,
        test_class
        ):
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    instance.pages.items_total = 0
    assert instance.items() == []


def test_implementation_items(dbsession, test_class):  # noqa: F811
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    assert len(instance.items()) == 12  # default number of items per page


def test_implementation_iter(dbsession, test_class):  # noqa: F811
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    assert instance.items() == list(instance)


@pytest.mark.parametrize(  # noqa: F811
    'field,direction,expected', [
        (None, None, ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        (None, 'asc', ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        (None, 'desc', ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        (None, 'unknown', ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        ('name', None, ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        ('name', 'asc', ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        ('name', 'desc', [
            'Ġbejna',
            'Époisses de Bourgogne',
            'Västerbottensost'
            ]
        ),
        ('name', 'unknown', ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        ('country', None, ['Passendale cheese', 'Remoudou', 'Rodoric']),
        ('country', 'asc', ['Passendale cheese', 'Remoudou', 'Rodoric']),
        ('country', 'desc', [
            'Guayanés cheese',
            'Colorado Blackie',
            'Red Hawk'
            ]
        ),
        ('country', 'unknown', ['Passendale cheese', 'Remoudou', 'Rodoric']),
        ('unknown', None, ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        ('unknown', 'asc', ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        ('unknown', 'desc', ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        ('unknown', 'unknown', ['Akkawi', 'Allgäuer Bergkäse', 'Areesh']),
        ]
    )
def test_implementation_ordered_query(
        dbsession,
        test_class,
        field,
        direction,
        expected
        ):
    get = {}
    if field is not None:
        get['o'] = field
    if direction is not None:
        get['d'] = direction
    request = DummyRequest(get, dbsession=dbsession)
    instance = test_class(request)
    items = instance.ordered_query.limit(3).offset(0).all()
    assert [item.name for item in items] == expected
    if field == 'country':
        assert instance.order_by == field
    else:
        assert instance.order_by == 'name'
    assert instance.order_dir in {'asc', 'desc'}


def test_implementation_order_direction(dbsession, test_class):  # noqa: F811
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    instance.order_dir = 'some value'
    assert instance.order_direction == 'some value'


def test_remember(dbsession, test_class):  # noqa: F811
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    instance.remember('some key', 'some value')
    assert instance.filters == {'some key': 'some value'}


def test_implementation_query_params(dbsession, test_class):  # noqa: F811
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    instance.pages.items_per_page = 1
    instance.pages.current = 2
    instance.order_by = 'some field'
    instance.order_dir = 'some direction'
    instance.filters = {'a filter': 'a value'}
    expected = {
        'n': 1,
        'p': 2,
        'o': 'some field',
        'd': 'some direction',
        'a filter': 'a value'
        }
    assert instance.query_params() == expected


def test_implementation_query_params_override(  # noqa: F811
        dbsession,
        test_class
        ):
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    instance.pages.items_per_page = 1
    instance.pages.current = 2
    instance.order_by = 'some field'
    instance.order_dir = 'some direction'
    instance.filters = {'a filter': 'a value'}
    expected = {
        'n': 10,
        'p': 20,
        'o': 'some field',
        'd': 'some direction',
        'a filter': 'a value'
        }
    assert instance.query_params(n=10, p=20) == expected


def test_implementation_query_params_removal_with_none(  # noqa: F811
        dbsession,
        test_class
        ):
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    instance.pages.items_per_page = 1
    instance.pages.current = 2
    instance.order_by = 'some field'
    instance.order_dir = 'some direction'
    instance.filters = {'a filter': 'a value'}
    expected = {
        'p': 2,
        'o': 'some field',
        'd': 'some direction',
        'a filter': 'a value'
        }
    assert instance.query_params(n=None) == expected


def test_implementation_call(dbsession, test_class):  # noqa: F811
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    instance.pages.items_per_page = 1
    instance.pages.current = 2
    assert instance.query_params(n=None) == instance(n=None)


def test_implementation_calculate_pagination_error(  # noqa: F811
        dbsession,
        test_class
        ):
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    instance.filtered_query = None
    with pytest.raises(NotImplementedError):
        instance.pages


def test_implementation_calculate_pagination(  # noqa: F811
        dbsession,
        test_class
        ):
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    assert instance.pages is not None
    assert instance.pages.items_total == 68

'''Tests for `pyramid_listing.resource` ListingResource class.'''

import pytest

from . import DummyRequest
from .database_fixture import Cheese, dbsession


class DummyModelResource:
    pass


@pytest.fixture
def test_class():
    from pyramid_listing.resource import ListingResource

    class TestImplementation(ListingResource):

        def __init__(self, request, name=None, parent=None):
            super().__init__(request, name, parent)
            self.default_order_by_field = 'name'
            self.default_order_by_direction = 'asc'

        def __getitem__(self, key):
            result = self.base_query.filter_by(name=key).first()
            if not result:
                raise KeyError
            return result

        def resource_from_model(self, model):
            return DummyModelResource()

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


def test_initialization(dbsession, test_class):
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request, 'some name', 'any parent')
    assert instance.__name__ == 'some name'
    assert instance.__parent__ == 'any parent'

def test_items(dbsession, test_class):
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    assert len(instance.items()) == 12  # default number of items per page
    for item in instance.items():
        assert isinstance(item, DummyModelResource)

def test_iter(dbsession, test_class):
    request = DummyRequest(dbsession=dbsession)
    instance = test_class(request)
    assert len(list(instance)) == 12  # default number of items per page
    for item in instance:
        assert isinstance(item, DummyModelResource)

def test_base_class_getitem_raises_error():
    from pyramid_listing.resource import ListingResource
    with pytest.raises(NotImplementedError):
        ListingResource.__getitem__(None, None)

def test_base_class_resource_from_model_raises_error():
    from pyramid_listing.resource import ListingResource
    with pytest.raises(NotImplementedError):
        ListingResource.resource_from_model(None, None)

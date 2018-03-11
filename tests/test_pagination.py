'''Tests for `pyramid_listing.pagination` Pagination class.'''

import pytest

from . import DummyRequest


@pytest.mark.parametrize(
    'data,key,default,expected', [
        ({}, 'x', 1, 1),
        ({'a': 2}, 'x', 1, 1),
        ({'x': 2}, 'x', 1, 2),
        ({'x': '123'}, 'x', 1, 123),
        ({'x': None}, 'x', 1, 1),
        ({'x': 'not a number'}, 'x', 1, 1)
        ]
    )
def test_get_as_int(data, key, default, expected):
    from pyramid_listing.pagination import get_as_int
    assert get_as_int(data, key, default) == expected


def test_pagination_init():
    from pyramid_listing.pagination import Pagination
    request = DummyRequest({'p': 2})
    pages = Pagination(request, 100)
    assert pages.items_total == 100
    assert pages.items_per_page is not None
    assert pages.first is not None
    assert pages.previous is not None
    assert pages.prev is not None
    assert pages.current is not None
    assert pages.next is not None
    assert pages.last is not None
    assert pages.window is not None
    assert pages.offset is not None
    assert pages.limit is not None


def test_pagination_init_with_no_items():
    from pyramid_listing.pagination import Pagination
    request = DummyRequest({'p': 2})
    pages = Pagination(request, 0)
    assert pages.items_total == 0
    assert pages.items_per_page is not None
    assert pages.first is None
    assert pages.previous is None
    assert pages.prev is None
    assert pages.current is None
    assert pages.next is None
    assert pages.last is None
    assert pages.window == []
    assert pages.offset == 0
    assert pages.limit == 0


@pytest.mark.parametrize(
    'get,expected',
    [({}, 12), ({'n': 25}, 25), ({'n': 'no number'}, 12)]
    )
def test_pagination_set_items_per_page_no_session(get, expected):
    from pyramid_listing.pagination import Pagination
    request = DummyRequest(get)
    pages = Pagination(request, 100)
    assert pages.items_per_page == expected


@pytest.mark.parametrize(
    'get,session,expected', [
        ({}, {}, 12),
        ({'n': 25}, {}, 25),
        ({'n': 'no number'}, {}, 12),
        ({}, {'items_per_page': 50}, 50),
        ({}, {'items_per_page': 'not a number'}, 12),
        ({'n': 25}, {'items_per_page': 50}, 25),
        ({'n': 'no number'}, {'items_per_page': 50}, 50),
        ({'n': 25}, {'items_per_page': 'not a number'}, 25),
        ({'n': 'no number'}, {'items_per_page': 'not a number'}, 12),
        ]
    )
def test_pagination_set_items_per_page_with_session(get, session, expected):
    from pyramid_listing.pagination import Pagination
    request = DummyRequest(get, session=session)
    pages = Pagination(request, 100)
    assert pages.items_per_page == expected
    assert request.session['items_per_page'] == expected


@pytest.mark.parametrize(
    'limit,items_per_page,expected', [
        (None, 0, 10),
        (None, 1, 1),
        (None, 123, 123),
        (50, 0, 10),
        (50, 1, 1),
        (50, 50, 50),
        (50, 51, 10),
        ({12, 24, 48}, 12, 12),
        ({12, 24, 48}, 24, 24),
        ({12, 24, 48}, 48, 48),
        ({12, 24, 48}, 0, 10),
        ({12, 24, 48}, 15, 10),
        ({12, 24, 48}, 51, 10),
        ]
    )
def test_check_items_per_page_limit(limit, items_per_page, expected):
    from pyramid_listing.pagination import Pagination
    request = DummyRequest()
    pages = Pagination(request, 100)
    pages.items_per_page_default = 10
    pages.items_per_page_limit = limit
    assert pages._check_items_per_page_limit(items_per_page) == expected


@pytest.mark.parametrize(
    'count, page, items, expected', [
        (1, 1, 3, [1, None, 1, None, 1]),
        (2, 1, 3, [1, None, 1, None, 1]),
        (3, 1, 3, [1, None, 1, None, 1]),
        (4, 1, 3, [1, None, 1, 2, 2]),
        (5, 1, 3, [1, None, 1, 2, 2]),
        (6, 1, 3, [1, None, 1, 2, 2]),
        (7, 1, 3, [1, None, 1, 2, 3]),
        (1, 1, 10, [1, None, 1, None, 1]),
        (2, 1, 10, [1, None, 1, None, 1]),
        (9, 1, 10, [1, None, 1, None, 1]),
        (10, 1, 10, [1, None, 1, None, 1]),
        (11, 1, 10, [1, None, 1, 2, 2]),
        (11, 2, 10, [1, 1, 2, None, 2]),
        (20, 2, 10, [1, 1, 2, None, 2]),
        (21, 2, 10, [1, 1, 2, 3, 3]),
        (100, 5, 10, [1, 4, 5, 6, 10]),
        (10, 5, 10, [1, None, 1, None, 1]),
        ]
    )
def test_pagination_calculate_page_numbers(count, page, items, expected):
    from pyramid_listing.pagination import Pagination
    request = DummyRequest({'p': page, 'n': items})
    pages = Pagination(request, count)
    assert pages.first == expected[0]
    assert pages.prev == pages.previous == expected[1]
    assert pages.current == expected[2]
    assert pages.next == expected[3]
    assert pages.last == expected[4]


@pytest.mark.parametrize(
    'count, page, left, right, expected', [
        (100, 1, 3, 3, [1, 2, 3, 4]),
        (100, 2, 3, 3, [1, 2, 3, 4, 5]),
        (100, 3, 3, 3, [1, 2, 3, 4, 5, 6]),
        (100, 4, 3, 3, [1, 2, 3, 4, 5, 6, 7]),
        (100, 5, 3, 3, [2, 3, 4, 5, 6, 7, 8]),
        (100, 6, 3, 3, [3, 4, 5, 6, 7, 8, 9]),
        (100, 7, 3, 3, [4, 5, 6, 7, 8, 9, 10]),
        (100, 8, 3, 3, [5, 6, 7, 8, 9, 10]),
        (100, 9, 3, 3, [6, 7, 8, 9, 10]),
        (100, 10, 3, 3, [7, 8, 9, 10]),
        (100, 1, 2, 2, [1, 2, 3]),
        (100, 2, 2, 2, [1, 2, 3, 4]),
        (100, 3, 2, 2, [1, 2, 3, 4, 5]),
        (100, 4, 2, 2, [2, 3, 4, 5, 6]),
        (100, 5, 2, 2, [3, 4, 5, 6, 7]),
        (100, 6, 2, 2, [4, 5, 6, 7, 8]),
        (100, 7, 2, 2, [5, 6, 7, 8, 9]),
        (100, 8, 2, 2, [6, 7, 8, 9, 10]),
        (100, 9, 2, 2, [7, 8, 9, 10]),
        (100, 10, 2, 2, [8, 9, 10]),
        (100, 1, 2, 3, [1, 2, 3, 4]),
        (100, 2, 2, 3, [1, 2, 3, 4, 5]),
        (100, 3, 2, 3, [1, 2, 3, 4, 5, 6]),
        (100, 4, 2, 3, [2, 3, 4, 5, 6, 7]),
        (100, 7, 3, 2, [4, 5, 6, 7, 8, 9]),
        (100, 8, 3, 2, [5, 6, 7, 8, 9, 10]),
        (100, 9, 3, 2, [6, 7, 8, 9, 10]),
        (100, 10, 3, 2, [7, 8, 9, 10]),
        ]
    )
def test_pagination_calculate_window(count, page, left, right, expected):
    ''' calculation of related pages '''
    from pyramid_listing.pagination import Pagination
    request = DummyRequest({'p': page, 'n': 10})
    Pagination.page_window_left = left
    Pagination.page_window_right = right
    pages = Pagination(request, count)
    assert pages.window == expected
    Pagination.page_window_left = 3
    Pagination.page_window_right = 3


@pytest.mark.parametrize(
    'first, last, check, expected', [
        (1, 1, 0, None),
        (1, 1, 1, 1),
        (1, 1, 2, None),
        (2, 4, 1, None),
        (2, 4, 2, 2),
        (2, 4, 3, 3),
        (2, 4, 4, 4),
        (2, 4, 5, None),
        ]
    )
def test_pagination_validate_page(first, last, check, expected):
    from pyramid_listing.pagination import Pagination
    request = DummyRequest()
    pages = Pagination(request, 1)
    pages.first = first
    pages.last = last
    assert pages.validate_page(check) == expected


def test_pagination_validate_page_returns_default():
    from pyramid_listing.pagination import Pagination
    request = DummyRequest()
    pages = Pagination(request, 1)
    assert pages.validate_page(2, 'default') == 'default'


def test_pagination_validate_page_returns_default_on_no_items():
    from pyramid_listing.pagination import Pagination
    request = DummyRequest()
    pages = Pagination(request, 0)
    pages.first = 1
    pages.last = 3
    assert pages.validate_page(2, 'default') == 'default'

'''Tests for `pyramid_listing.pagination` includeme() function.

These tests are separate from the `pyramid_listing.pagination` tests
to provide isolation while configuring the pagination class
'''

import pytest

from . import DummyConfig


@pytest.mark.parametrize(
    'key,value', [
        ('items_per_page_default', 123),
        ('page_window_left', 12),
        ('page_window_right', 15)
        ]
    )
def test_includeme_simple_settings(key, value):
    from pyramid_listing import pagination
    remember = getattr(pagination.Pagination, key)
    config = DummyConfig({key: value})
    pagination.includeme(config)
    assert getattr(pagination.Pagination, key) == value
    setattr(pagination.Pagination, key, remember)


def test_includeme_window_size_setting():
    from pyramid_listing import pagination
    config = DummyConfig({'page_window_size': 11})
    pagination.includeme(config)
    assert pagination.Pagination.page_window_left == 5
    assert pagination.Pagination.page_window_right == 5


def test_includeme_asymetric_window_precedence_over_window_size():
    from pyramid_listing import pagination
    config = DummyConfig({
        'page_window_left': 2,
        'page_window_right': 7,
        'page_window_size': 11,
        })
    pagination.includeme(config)
    assert pagination.Pagination.page_window_left == 2
    assert pagination.Pagination.page_window_right == 7

@pytest.mark.parametrize(
    'limit,expected', [
        (42, 42),
        ([12, 24, 48], {12, 24, 48})
        ]
    )
def test_items_per_page_limit(limit, expected):
    from pyramid_listing import pagination
    config = DummyConfig({'items_per_page_limit': limit})
    pagination.includeme(config)
    assert pagination.Pagination.items_per_page_limit == expected

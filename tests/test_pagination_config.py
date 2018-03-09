'''Tests for `pyramid_listing.pagination` includeme() function.

These tests are separate from the `pyramid_listing.pagination` tests
to provide isolation while configuring the pagination class
'''

import pytest

from . import DummyConfig, DummyRequest

@pytest.mark.parametrize(
    'key,value',[
        ('current_page_request_key', 'test_cprk'),
        ('items_per_page_default', 123),
        ('items_per_page_request_key', 'test_ipprk'),
        ('items_per_page_session_key', 'test_ippsk'),
        ('page_window_left', 12),
        ('page_window_right', 15)
        ]
    )
def test_includeme_simple_settings(key, value):
    from pyramid_listing import pagination
    config = DummyConfig({key: value})
    pagination.includeme(config)
    assert getattr(pagination.Pagination, key) == value


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

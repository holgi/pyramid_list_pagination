'''Tests for `pyramid_listing.pagination` includeme() function.

These tests are separate from the `pyramid_listing.pagination` tests
to provide isolation while configuring the pagination class
'''

import pytest

from . import DummyConfig


@pytest.fixture(scope='function')
def test_class():
    from pyramid_listing.pagination import Pagination

    class ConfigTestClass(Pagination):
        pass

    yield ConfigTestClass


@pytest.mark.parametrize(
    'key,value', [
        ('items_per_page_default', 123),
        ('page_window_left', 12),
        ('page_window_right', 15),
        ('items_per_page_default', '123'),
        ('page_window_left', '12'),
        ('page_window_right', '15')
        ]
    )
def test_configure_simple_settings(test_class, key, value):
    test_class.configure({'pyramid_listing.' + key: value})
    assert getattr(test_class, key) == int(value)


@pytest.mark.parametrize('size', [11, '11'])
def test_configure_window_size_setting(test_class, size):
    test_class.configure({'pyramid_listing.page_window_size': size})
    assert test_class.page_window_left == 5
    assert test_class.page_window_right == 5


def test_configure_asymetric_window_precedence_over_size(test_class):
    config = {
        'pyramid_listing.page_window_left': 2,
        'pyramid_listing.page_window_right': 7,
        'pyramid_listing.page_window_size': 11,
        }
    test_class.configure(config)
    assert test_class.page_window_left == 2
    assert test_class.page_window_right == 7


@pytest.mark.parametrize(
    'limit,expected', [
        (42, 42),
        ('42', 42),
        ([12, 24, 48], {12, 24, 48}),
        (['13', '25', '49'], {13, 25, 49}),
        ('12 24 48', {12, 24, 48})
        ]
    )
def test_configure_items_per_page_limit(test_class, limit, expected):
    test_class.configure({'pyramid_listing.items_per_page_limit': limit})
    assert test_class.items_per_page_limit == expected


def test_configure_different_prefix(test_class):
    test_class.configure({'pl.page_window_size': 11}, prefix='pl.')
    assert test_class.page_window_left == 5


def test_include_me():
    from pyramid_listing import pagination
    remember = pagination.Pagination.items_per_page_default
    config = DummyConfig({'items_per_page_default': 123})
    pagination.includeme(config)
    assert pagination.Pagination.items_per_page_default == 123
    pagination.Pagination.items_per_page_default = remember

'''Tests for `pyramid_listing.__init__.py` module.'''


from . import DummyConfig


def test_imports():
    from pyramid_listing import includeme  # noqa: F401
    from pyramid_listing import Pagination  # noqa: F401
    from pyramid_listing import SQLAlchemyListing  # noqa: F401
    from pyramid_listing import ListingResource  # noqa: F401


def test_include_me():
    from pyramid_listing import includeme, Pagination
    from pyramid_listing import pagination
    remember = pagination.Pagination.items_per_page_default
    config = DummyConfig({'items_per_page_default': 123})
    includeme(config)
    assert Pagination.items_per_page_default == 123
    assert pagination.Pagination.items_per_page_default == 123
    pagination.Pagination.items_per_page_default = remember

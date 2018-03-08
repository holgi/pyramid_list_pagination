'''Tests for `pyramid_list_pagination` package.'''

import pytest


class DummyConfig:

    def __init__(self, settings, prefix='list_pagination'):
        self.settings = {f'{prefix}.{k}': v for k, v in settings.items()}

    def get_settings(self):
        return self.settings


class DummyRequest:

    def __init__(self, data=None, session=None):
        self.GET = data or {}
        if session is not None:
            self.session = session

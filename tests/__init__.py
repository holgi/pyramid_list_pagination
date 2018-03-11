'''Tests for `pyramid_listing` package.'''


class DummyConfig:

    def __init__(self, settings, prefix='pyramid_listing'):
        self.settings = {f'{prefix}.{k}': v for k, v in settings.items()}

    def get_settings(self):
        return self.settings


class DummyRequest:

    def __init__(self, data=None, dbsession=None, session=None):
        self.GET = data or {}
        self.dbsession = dbsession
        # only add a session property, if there is a session
        # this emulates a pyramid application without session object
        if session is not None:
            self.session = session

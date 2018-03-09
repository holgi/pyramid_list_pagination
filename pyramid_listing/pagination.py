''' Pagination - calculate pagination information '''


def get_as_int(store, key, default):
    try:
        value = store.get(key, default)
        return int(value)
    except (ValueError, TypeError):
        return default


class Pagination:
    ''' calculates pagination information

    :param pyramid.Request request: request object
    :param int items_total: total number of items

    :ivar int items_total: total number of items
    :ivar int items_per_page: number of items to show on one page
    :ivar int first: first page number
    :ivar int previous: previous page number, same as ``prev``
    :ivar int prev: previous page number, same as ``previous``
    :ivar int current: current page number
    :ivar int next: next page number
    :ivar int last: last page number
    :ivar list window: page window
    :ivar int offset: offset parameter for a sql query
    :ivar int limit: limit parameter for a sql query

    The settings for the pagination, like how many items should be shown on one
    page can be configured in the pyramid .ini file with these parameters (and
    defaults):

    Number of items shown on a result page:
    ``list_pagination.items_per_page_default = 12``

    If session is configured in the pyramid app, it is used to store the number
    of items to show per page. So, if a visitor makes a selection for items per
    page, it can be retrieved as soon as the visitor accesses another list.
    This removes the (for me) annoying situation, where I need to reconfigure
    my items per page setting as soon as I select another category on a
    shopping site.
    If a session is not used in the pyramid app, this setting is ignored.
    If you don't want to use the session to store this information, set the
    ``items_per_page_session_key`` value to an empty string.

    A pagination window shows you some page numbers before and after the
    current page. For an example,  lets assume the current page is 10 and
    the size is 7, so the page window will be a list consisting of these
    numbers: 7, 8, 9, 10, 11, 12, 13

    To be able to configure asymetric windows, e.g. two pages before the
    current page and five pages afterwards, there are two settings:
    ``list_pagination.page_window_left = 3`` and
    ``list_pagination.page_window_right = 3``

    If you just want a symetric window, you could also specify just one value
    ``list_pagination.page_window_size``. If assymetric and simple size are
    defined, the asymetric definition takes precedence.
    '''

    #: Request.GET key for the page to show
    current_page_request_key = 'p'

    #: Number of items shown on a result page
    items_per_page_default = 12

    #: Request.GET key for the number of items shown on a page
    items_per_page_request_key = 'n'

    #: Name of session variable to store the number of items shown on a page
    items_per_page_session_key = 'items_per_page'

    #: number of pages to the left on a page window
    page_window_left = 3

    #: number of pages to the left on a page window
    page_window_right = 3


    def __init__(self, request, items_total):
        ''' initialization

        :param pyramid.Request request: request object
        :param int items_total: total number of items
        '''
        items_total = int(items_total)
        items_total = 0 if items_total < 1 else items_total
        self.items_total = items_total  #: total number of items
        self.items_per_page = None  #: number of items to show on one page

        self.first = None  #: first page number
        self.previous = None  #: previous page number, same as ``prev``
        self.prev = None  #: previous page number, same as ``previous``
        self.current = None  #: current page number
        self.next = None  #: next page number
        self.last = None  #: last page number

        self.window = []  #: page window

        self.offset = 0  #: offset parameter for a sql query
        self.limit = 0  #: limit parameter for a sql query

        self._set_items_per_page(request)
        page_nr = get_as_int(request.GET, self.current_page_request_key, 1)
        self.calculate(page_nr)


    def _set_items_per_page(self, request):
        ''' set number of items per page from session and / or request

        :param pyramid.Request request: request object

        If a session is not used, only the request would be queried.

        If a session is used, the value of the session is only used, if
        the request object does not specifiy a value. In either case, the
        current number of items is stored again in the session.
        '''
        if hasattr(request, 'session') and self.items_per_page_session_key:
            items_per_page_from_session = get_as_int(
                request.session,
                self.items_per_page_session_key,
                self.items_per_page_default
                )
            items_per_page = get_as_int(
                request.GET,
                self.items_per_page_request_key,
                items_per_page_from_session
                )
            request.session[self.items_per_page_session_key] = items_per_page
            self.items_per_page = items_per_page
        else:
            self.items_per_page = get_as_int(
                request.GET,
                self.items_per_page_request_key,
                self.items_per_page_default
                )

    def calculate(self, requested_page):
        ''' calcualte all the values! '''
        # if there are no items to display, there is no need for a calculation
        if not self.items_total:
            return
        # calculate the first and last page. This is needed to check if a page
        # number is valid
        self.first = 1
        self.last = (self.items_total - 1) // self.items_per_page + 1

        # set the current page number
        self.current = self.validate_page(requested_page, self.first)

        # the previous and next page
        self.previous = self.validate_page((self.current - 1), None)
        self.prev = self.previous
        self.next = self.validate_page((self.current + 1), None)

        # calculate the page window
        start = self.current - self.page_window_left
        end = self.current + self.page_window_right
        full_window = range(start, end + 1)
        self.window = [p for p in full_window if self.validate_page(p, None)]

        # offset and limit for sql queries
        self.offset = (self.current - 1) * self.items_per_page
        self.limit = self.items_per_page

    def validate_page(self, page, default=None):
        ''' checks if a page is not outside first and last page '''
        if self.items_total and self.first <= page <= self.last:
            return page
        return default


def includeme(config):
    ''' configure the pagination settings from a pyramid .ini file

    The available configuration settings are listed below::

        [app:main]
        list_pagination.items_per_page_default = 12
        list_pagination.page_window_left = 3
        list_pagination.page_window_right = 3

    Instead of defining ``page_window_left`` and ``page_window_right``,
    a single integer value for ``page_window_size`` can be specified for
    a symetric page window
    '''
    settings = config.get_settings()
    prefix = 'pyramid_listing'

    # set the right values if a simple page window size is given
    window_size = settings.get(f'{prefix}.page_window_size', None)
    if window_size is not None:
        window_size = int(window_size)
        half_window = window_size // 2
        Pagination.page_window_left = half_window
        Pagination.page_window_right = half_window

    # transfer the available settings to the pagination class
    items = ['items_per_page_default', 'page_window_left', 'page_window_right']
    for what in items:
        value = settings.get(f'{prefix}.{what}', None)
        if value is not None:
            setattr(Pagination, what, int(value))

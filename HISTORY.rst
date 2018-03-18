=======
History
=======

0.1.8 (2018-03-18)
------------------
* changed SQLAlchemyListing.pages to a calculated property:

  Just creating a SQLAlchemyListing instance does not automatically trigger
  a database query. It will only execute this first query if pagination
  information is accessed, e.g. in a ordered query.


0.1.7 (2018-03-14)
------------------
* applied filters can now be accessed via ``SQLAlchemyListing.filters``


0.1.6 (2018-03-13)
------------------
* updated documentation setup for readthedocs.org


0.1.5 (2018-03-13)
------------------
* code adjustments after liniting


0.1.4 (2018-03-13)
------------------
* fixed bug where settings as strings were not parsed correctly
* changed default implementation of __getitem__() to use base_query
* changed ordered_query from a calculated property to a real one


0.1.3 (2018-03-12)
------------------

* The classes and the includeme() function are now exposed in the __init__.py
  file


0.1.2 (2018-03-12)
------------------

* The pagination calculation class can now be configured in ``Listing`` and
  ``Resource`` classes. This enables the use of different pagination defaults
  in different lists.


0.1.1 (2018-03-12)
------------------

* Untangled Pagination configuration from includeme() function. Pagination
  (sub-) classes can now be configured via the ``configure()`` method


0.1.0 (2018-03-11)
------------------

* First Working Implementation


0.0.1 (2018-03-08)
------------------

* Starting the project

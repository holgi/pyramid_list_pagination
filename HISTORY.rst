=======
History
=======

0.1.5 (2018-03-13)
-----------------
* code adjustments after liniting


0.1.4 (2018-03-13)
-----------------
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

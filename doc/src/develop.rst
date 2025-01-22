.. _sec-contribute:

Contribute to snowprofile
=========================

Developer environment
---------------------

Any contributor must:

* use the **git** versioning tool 
* work in a branch, deriving from either the latest ``master`` or ``dev`` branches.
* Test before commit (see below)
* Ensure new development have a corresponding test
* Ensure new development have a corresponding documentation
* Ensure you followed guidelines below

Code style
----------

Python code should comply with PEP8 https://www.python.org/dev/peps/pep-0008 style guide. Please check your code before committing.
In particular, tabs are prohibited and lines may not exceed 120 characters.

Shebangs
^^^^^^^^

Moreover, **all** codes must specify the encoding, which have to be ``utf-8``:

.. code-block:: python
   
   # -*- coding: utf-8 -*-

Imports
^^^^^^^

Please avoid relative imports in snowprofile.

See PEP 8 import section https://www.python.org/dev/peps/pep-0008/#imports for more details on correct import order and other guidelines on imports.

Of course star-imports (``from XXX import *``) are prohibited.

Language
--------

Of course, all comments in the code, documentation and commit message have to be in english.

Tests
-----
To ensure backward compatibility and maintainability of the code, the ``snowprofile`` package comes with a test suite.

To run the tests, just go the the ``snowprofile`` code repository and run ``python3 -m pytest``.

When developping, please run the test base before each commit and ensure that new developments come with new tests.

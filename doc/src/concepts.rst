.. _concepts:

Main concepts of this package
=============================

The whole package is organized around the creation and manipulation of ``SnowProfile`` data class.

Looking inside
--------------

To have an overview of the content of a ``SnowProfile`` object, you can use ``rich`` package:


.. code-block:: python

   import snowprofile
   sp = snowprofile.SnowProfile()
   from rich import print as rprint
   rprint(sp)


We plan to provide a dedicated tool in the future.

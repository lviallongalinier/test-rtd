Have an overview of the content of a ``SnowProfile``
====================================================

Look at the SnowProfile object
-------------------------------

To have an overview of the content of a ``SnowProfile`` object, you can use the ``rich`` package:

.. code-block:: python

   import snowprofile
   sp = snowprofile.SnowProfile()
   from rich import print as rprint
   rprint(sp)


Plot profiles
-------------

To plot the content of a SnowProfile object, the following function can be used: :py:func:`snowprofile.plot.plot_snowprofile.plot_snowprofile`


For example, run:

.. code-block:: python

   import snowprofile
   filename = 'path/to/caaml_file.caaml'
   plot_snowprofile(filename, style_ssa_profiles='step', style_hardness_profiles='step',
    index_ssa_profiles=[0, 1], style_hardness_profiles='point', lw = 2)


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

To plot the content of a SnowProfile object, the following functions can be used: :py:func:`snowprofile.plot.plot_simple` or :py:func:`snowprofile.plot.plot_full`. See :ref:`plot` for more details.


For example, run:

.. code-block:: python

   import matplotlib.pyplot as plt
   import snowprofile
   import snowprofile.plot
   filename = 'path/to/caaml_file.caaml'
   sp = snowprofile.io.read_caaml6_xml(filename)
   snowprofile.plot.plot_full(filename)
   plt.show()

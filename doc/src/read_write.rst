Read, write and merge profiles
==============================

Start a new profile from scratch
--------------------------------

To create a new blank SnowProfile object, in which to add your data, run:

.. code-block:: python

   import snowprofile
   sp = snowprofile.SnowProfile()


The dataset created has no name, and the spatial location and time are the default. You have to set the correct information:

- Set the location:

.. code-block:: python

   sp.location.name = 'Col de Porte'
   sp.location.latitude = 45.295043
   sp.location.longitude = 5.76559

- Set the observation time:


.. code-block:: python

   import datetime
   sp.time.record_time = datetime.datetime(2019, 12, 25, 10, 0)
   sp.time.report_time = datetime.datetime.now()

To add an observed density profile, first create the profile and then add it to the SnowProfile object:

.. code-block:: python

   dp = snowprofile.profiles.DensityProfile(
       method_of_measurement="Snow Cutter",
       quality_of_measurement="Good",
       probed_thickness=0.03,  # 3cm cutter thickness
       data = {'top_height': [1.2, 1.1, 1, 0.5],
               'thickness': [0.1, 0.1, 0.5, 0.5],
               'density': [75, 100, 180, 230]}
   )
   sp.density_profiles.append(dp)

To modify a profile, you have to re-assign the dataframe to the data key of the profile otherwise the changes are not taken into account:


.. code-block:: python

   df = dp.data
   # Let's put a little bit more snow on the ground!
   df['thickness'] *= 2
   df['top_height'] *= 2
   dp.data = df[['thickness', 'top_height', 'density']]


Read an existing CAAML file
---------------------------

.. CAAML snow profiles can be edited with `Niviz <https://www.niviz.org/>`_. This package allow for manipulation of such observations with python. It can be used for automatic python processing, adding metadata that are not covered by Niviz or combination of different data sources.

If you have an existing .caaml file, created with `Niviz <https://www.niviz.org/>`_ for example, you can open it, modify it or add more data to it (such as the data that could not be entered with Niviz). Reading your .caaml file with the SnowProfile package also gives you the option of processing your data using python code, as your data is converted into a python object.

To open an existing CAAML file:

.. code-block:: python

   import snowprofile.io
   filename = 'path/to/caaml_file.caaml'
   sp = snowprofile.io.read_caaml6_xml(filename)


.. The description of on reading and writing CAAML files are available in :ref:`io`. Other formats for getting and writing data are also supported.

See :ref:`io` for details.

Merge data
----------

To combine two souces of data of the same measurement set, when loaded as two ``SnowProfile`` elements, ``sp1`` and ``sp2``, run:

.. code-block:: python

   sp1.merge(sp2)

See :py:func:`snowprofile.SnowProfile.merge` for details.

Write a CAAML file
------------------

To save your ``SnowProfile`` object called ``sp``, run:

.. code-block:: python

   import snowprofile.io
   filename = 'path/to/my_new_caaml_file.caaml'
   version = 'version='6.0.5'
   snowprofile.io.write_caaml6_xml(sp, filename, version)

See :ref:`io` for details.

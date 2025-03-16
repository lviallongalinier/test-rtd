Use case examples
=================

Start a new profile from zero
-----------------------------

To create a new blank profile to further add data inside, run :

.. code-block:: python

   import snowprofile
   sp = snowprofile.SnowProfile()

The created profile does not have any name and the spatial localization is more or less random. You have to edit anything relevant, for instance:

- Set the correct location:

.. code-block:: python

   sp.location.name = 'Col de Porte'
   sp.location.latitude = 45.295043
   sp.location.longitude = 5.76559

- Set the correct observation time:


.. code-block:: python

   import datetime
   sp.time.record_time = datetime.datetime(2019, 12, 25, 10, 0)
   sp.time.report_time = datetime.datetime.now()

- To add an observed density profile, first create the profile and then add to the SnowProfile object:

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

NB : when changing data, you have to re-assign the dataframe to the data key of the profile otherwise the changes are not taken into account:


.. code-block:: python

   df = dp.data
   # Let's put a little bit more of snow on ground!
   df['thickness'] *= 2
   df['top_height'] *= 2
   dp.data = df[['thickness', 'top_height', 'density']]


Read and write CAAML snowprofiles
---------------------------------

CAAML snow profiles can be edited with `Niviz <https://www.niviz.org/>`_. This package allow for manipulation of such observations with python. It can be used for automatic python processing, adding metadata that are not covered by Niviz or combination of different data sources.

The package allow to open an existing CAAML file :

.. code-block:: python

   import snowprofile.io
   filename = 'path/to/caaml_file.caaml'
   sp = snowprofile.io.read_caaml6_xml(filename)

More details on reading and writing CAAML files are available in :ref:`io`. Other formats for getting and writing data are also supported.

Combine different data sources
------------------------------

It is possible to combine different data sources. When loaded as two ``SnowProfile`` elements, ``sp1`` and ``sp2``, just do:

.. code-block:: python

   sp1.merge(sp2)

See :py:func:`snowprofile.SnowProfile.merge` for details.


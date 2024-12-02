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
       data = {'top_depth': [120, 110, 100, 50],
               'thickness': [10, 10, 50, 50],
               'density': [75, 100, 180, 230]}
   )
   sp.density_profiles.append(dp)

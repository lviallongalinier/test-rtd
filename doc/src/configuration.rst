.. _configuration:

Configuration of snowprofile package
====================================

Some parts of ``snowprofile`` package can be adapted to each user. The configuration is done in a ini file located:

- On UNIX systems, the config file is located in ``~/.config/snowprofile.ini``
- On Windows systems, the config file is directly in user home directory with the same name

In a ``[DEFAULT]`` section are stored keys common to all parts of the code while other sections could be used by sub-parts of the code.

It contains:

- The default observer configuration (when not provided, the default are used by readers)

Example file:

.. code-block:: ini

   [DEFAULT]
   observer_id= CEN
   observer_name = Univ. Grenoble Alpes, Université de Toulouse, Météo-France, CNRS, CNRM, Centre d'Études de la Neige, Grenoble, France
   observer_comment = The best laboratory on the Earth
   contact_person_id = 007
   contact_person_name = M. Hide
   contact_person_

If you plan to use :py:func:`snowprofile.io.read_mf_bdclim`, you have to create the folloing section:

.. code-block:: ini

   [io_mf_bdclim]
   host = host.domain.ext
   dbname = database_name
   user = username
   password = password

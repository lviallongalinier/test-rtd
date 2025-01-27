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
   contact_person = M. Hide


Auto Behave
===========

A sphinx extension for behave to auto document.

Setup
-----

To add auto behave to your sphinx modify :code:`conf.py` by adding auto behave to extensions like so:


.. code-block:: python

    extensions = ['..', '..', 'auto_behave']

To enable auto behave's rst generation modify :code:`conf.py` by adding the following to the bottom:

.. code-block:: python

    from auto_behave.gen_step_rst import generate_step_rst_files
    generate_step_rst_files('abs/path/to/project', 'rel/path/features/dir', 'rel/path/doc/features')

File Layout
-----------

Auto behave's rst generation supports both the standard behave & more custom folder structure layouts.

Standard Behave
^^^^^^^^^^^^^^^

.. code-block::

    features
    ├── environment.py
    ├── order.feature
    │
    └── steps
        ├── add.py
        └── remove.py

Custom Folder Structure
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    features
    ├── environment.py
    ├── order
    |   ├── create_order.feature
    │   └── steps
    |       ├── add.py
    |       └── remove.py
    |
    └── steps
        ├── __init__.py
        ├── navigation.py
        └── common.py

By default behave doesn't allow you to have step files in different directories outside a single step folder. Being locked to single folder becomes a problem with a large scale project. To get around behave's limitation within behave's step directory i.e.
:code:`features/steps` create :code:`__init__.py` and import all other steps files that are not in this directory i.e.

.. code-block:: python

    # features/steps/__init__.py

    import features.order.steps.add
    import features.order.steps.remove

Usage
-----

You can of course create your own rst for more manual approach by using autobehave directive, like so:

.. code-block:: shell

    Order Steps
    ===========

    ..  autobehave::

        features.order.steps.add
        features.order.steps.remove
Installation Guide
==================

BEEhaviourLab is distributed as a Python package.

Using pip
---------

To install the latest stable release from PyPI:

.. code-block:: bash

   pip install beehaviourlab

Alternatively, install with packages to generate docs or to run tests:

.. code-block:: bash

   pip install "beehaviourlab[docs]"
   pip install "beehaviourlab[test]"

To install with all extras (docs + tests):

.. code-block:: bash

   pip install "beehaviourlab[dev]"


To install an editable package from source (recommended for development):

.. code-block:: bash

   git clone https://github.com/BEEhaviourLab/BEEhaviourLab.git
   cd BEEhaviourLab
   pip install -e .

From source
-----------

Installation from source with packages for generating docs:

.. code-block:: bash

   pip install -e ".[docs]"

This will install Sphinx and other dependencies required to build the
documentation.

To build the docs locally:

.. code-block:: bash

   sphinx-build -b html docs docs/_build/html

The generated HTML can be found in ``docs/_build/html``.

To install with test dependencies, or both docs and test dependencies:

.. code-block:: bash

   pip install -e ".[test]"
   pip install -e ".[dev]"

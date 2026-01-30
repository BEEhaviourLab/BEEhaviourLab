Installation Guide
==================

BEEhaviourLab is distributed as a Python package. For now, the recommended
approach is to install from source.

From source (editable):

.. code-block:: bash

   git clone https://github.com/BEEhaviourLab/BEEhaviourLab.git
   cd BEEhaviourLab
   pip install -e .

Documentation dependencies:

.. code-block:: bash

   pip install -e ".[docs]"

This will install Sphinx and other dependencies required to build the
documentation.

Build the docs locally:

.. code-block:: bash

   sphinx-build -b html docs docs/_build/html

The generated HTML can be found in ``docs/_build/html``.

Test dependencies:

.. code-block:: bash

   pip install -e ".[test]"

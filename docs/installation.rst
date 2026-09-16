Installation & Requirements
============================

Prerequisites
-------------

- Python **3.9** or later (``python_requires = >=3.9`` in :file:`setup.cfg`).
- `skyfield <https://rhodesmill.org/skyfield/>`_ ``>=1.40,<2a0`` — the only
  third-party runtime dependency, used by :mod:`gifts.swaDecoder` for
  astronomical calculations (day/night terminator, sun/moon position) needed
  to encode Space Weather Advisories.

Installing from source
-----------------------

.. code-block:: shell

   $ git clone https://github.com/NOAA-MDL/GIFTs.git
   $ cd GIFTs
   $ python setup.py install

If you cannot install into the system ``site-packages``, add the checkout
directory to ``PYTHONPATH`` instead.

Installing test/lint extras
-----------------------------

.. code-block:: shell

   $ pip install .[test]

This installs ``pytest>=8.3``, ``pytest-cov>=2.7,<3a0``, and
``flake8>=3.7,<4a0`` as declared in the ``[options.extras_require]`` section
of :file:`setup.cfg`.

Configuration before first use
--------------------------------

1. **XML configuration** — review :file:`gifts/common/xmlConfig.py`. It
   controls IWXXM version/release strings, translator mode, vertical datum
   and elevation units, xlink title behavior, and visibility/RVR thresholds.
   See :doc:`data_mappings` for details.
2. **Geo-location database** — METAR/SPECI and TAF encoders require a
   caller-supplied object exposing a ``.get(icaoID)`` method that resolves an
   ICAO identifier to aerodrome metadata. See
   :doc:`data_mappings` and :file:`gifts/database/README.md` for how to build
   one from the bundled :file:`aerodromes.tbl` sample.

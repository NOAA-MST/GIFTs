Installation & Requirements
============================

Prerequisites
-------------

- Python **3.9** or later (``requires-python = ">=3.9"`` in :file:`pyproject.toml`).
- `skyfield <https://rhodesmill.org/skyfield/>`_ ``>=1.40,<2a0`` — the only
  third-party runtime dependency, used by :mod:`gifts.swaDecoder` for
  astronomical calculations (day/night terminator, sun/moon position) needed
  to encode Space Weather Advisories.

Installing from source
-----------------------

.. code-block:: shell

   $ git clone https://github.com/NOAA-MDL/GIFTs.git
   $ cd GIFTs
   $ pip install .

If you cannot install into the system ``site-packages``, add the checkout
directory to ``PYTHONPATH`` instead.

Installing test/lint/docs extras
-----------------------------------

.. code-block:: shell

   $ pip install .[test]
   $ pip install .[docs]

``.[test]`` installs ``pytest>=8.3``, ``pytest-cov>=2.7,<3a0``, and
``flake8>=3.7,<4a0``; ``.[docs]`` installs ``sphinx``, ``sphinx-rtd-theme``,
and ``myst-parser``, as declared in the ``[project.optional-dependencies]``
section of :file:`pyproject.toml`.

Skyfield bsp_files directory
-------------------------------

If :mod:`gifts.swaDecoder` fails to write ephemeris files due to permissions
on skyfield's ``bsp_files`` cache directory, run the following once after
installing:

.. code-block:: shell

   $ python scripts/setup_skyfield_bsp.py

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

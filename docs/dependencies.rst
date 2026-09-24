Dependencies
=============

Runtime (Python)
-------------------

.. list-table::
   :header-rows: 1

   * - Package
     - Constraint
     - Used by
     - Purpose
   * - `skyfield <https://rhodesmill.org/skyfield/>`_
     - ``>=1.40,<2a0``
     - :mod:`gifts.swaDecoder`
     - Astronomical calculations (sun/moon position, day/night terminator)
       for Space Weather Advisory encoding.
   * - ``tpg`` (bundled, :mod:`gifts.common.tpg`)
     - v3.2.4, vendored — not a pip dependency
     - all decoders
     - Toy Parser Generator: builds recursive-descent parsers from grammars
       embedded in class docstrings. LGPL-licensed.
   * - Python standard library
     - ``xml.etree.ElementTree``, ``re``, ``logging``, ``datetime``/``time``,
       ``pickle``, ``uuid``, ``gzip``, ``math``
     - throughout
     - XML construction, regex parsing, timestamps, aerodrome DB
       serialization, GML id generation, bulletin compression.

Test/lint (optional, ``pip install .[test]``)
-------------------------------------------------

- ``pytest>=8.3``
- ``pytest-cov>=2.7,<3a0``
- ``flake8>=3.7,<4a0`` (max line length 120, configured in :file:`.flake8`)

Docs (optional, ``pip install .[docs]``)
-------------------------------------------------

- ``sphinx>=7.0``
- ``sphinx-rtd-theme>=2.0``
- ``myst-parser>=2.0``

Validation tooling (separate from the library, ``validation/``)
--------------------------------------------------------------------

- Java **CRUX** ``v1.3`` (bundled jar,
  :file:`validation/bin/crux-1.3-all.jar`) — performs XSD + Schematron
  validation. See `NCAR/crux <https://github.com/NCAR/crux>`_.
- Python ``lxml`` and ``requests`` — parse XML and fetch schemas/RDF files
  on demand.
- Cached external XML Schemas under
  :file:`validation/externalSchemas/`: AIXM 5.1/5.1.1 (aero), GML 3.2.1,
  OGC ISO 19139, OM 2.0, SWE Common 2.0, sampling/samplingSpatial 2.0, WMO
  metce/opm/saf/collect schemas and schematron rules, and W3C XML
  namespace/XSD documents.

External standards referenced (non-code dependencies)
------------------------------------------------------------

- **ICAO Annex 3** — *Meteorological Service for International Air
  Navigation* — defines the legacy TAC formats decoded by GIFTs.
- **IWXXM** — ICAO Meteorological Information Exchange Model, jointly
  hosted by WMO/ICAO at
  `schemas.wmo.int/iwxxm <https://schemas.wmo.int/iwxxm/>`_ — defines the
  XML schemas GIFTs encodes into.
- **WMO code registries** — `codes.wmo.int <http://codes.wmo.int/>`_ —
  source of the RDF vocabularies bundled in :file:`gifts/data/`.
- **AIXM** — Aeronautical Information Exchange Model — describes aerodrome
  features referenced inside IWXXM METAR/TAF documents.
- **GML 3.2.1** — OGC Geography Markup Language — used for all spatial
  geometry (points, surfaces) in generated documents.
- **WMO Collect schema** (``http://def.wmo.int/collect/2014``) — defines the
  ``<MeteorologicalBulletin>`` wrapper produced by
  :meth:`gifts.common.bulletin.Bulletin.write`.

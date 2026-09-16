Overview & Capabilities
========================

What GIFTs does
----------------

GIFTs converts five classes of aviation weather TAC (Traditional Alphanumeric
Code) bulletins into IWXXM XML documents:

.. list-table::
   :header-rows: 1

   * - Product
     - Input TAC form
     - Output IWXXM root element
     - Requires geo-location DB?
   * - METAR / SPECI
     - ``METAR``/``SPECI`` observation
     - ``iwxxm:METAR`` / ``iwxxm:SPECI``
     - Yes (aerodrome lookup)
   * - TAF
     - ``TAF`` forecast
     - ``iwxxm:TAF``
     - Yes (aerodrome lookup)
   * - Space Weather Advisory (SWA)
     - ``SWX ADVISORY``
     - ``SpaceWeatherAdvisory``
     - No
   * - Tropical Cyclone Advisory (TCA)
     - ``TC ADVISORY``
     - ``TropicalCycloneAdvisory``
     - No
   * - Volcanic Ash Advisory (VAA)
     - ``VA ADVISORY``
     - ``VolcanicAshAdvisory``
     - No

Each product has a **decoder** (parses the TAC text into a Python ``dict``)
and an **encoder** (renders that ``dict`` as an IWXXM XML :class:`xml.etree.ElementTree.Element`
tree), orchestrated by a shared :class:`~gifts.common.Encoder.Encoder` base class
and returned to the caller wrapped in a
:class:`~gifts.common.bulletin.Bulletin` container.

What GIFTs produces
--------------------

- IWXXM XML documents (currently targeting IWXXM version ``2025-2``,
  schema release ``2025-2RC1``) for each decoded TAC report.
- A ``<MeteorologicalBulletin>`` XML wrapper document (WMO Collect schema,
  ``http://def.wmo.int/collect/2014``) suitable for transmission over the
  Extended AMHS as a File Transfer Body Part, optionally gzip-compressed.

What GIFTs does not do
-----------------------

- It does not fetch or receive TAC bulletins itself — text input is supplied
  by the caller (e.g. read from a file, a message queue, or a GTS feed).
- It does not perform schema/schematron validation of its own output; that is
  a separate concern handled by the tools in ``validation/`` (see
  :doc:`validation`).
- It does not ship a production-ready aerodrome database; it ships a sample
  flat file and a script to build a minimal one (see :doc:`data_mappings`).

Who this is for
-----------------

Meteorological Watch Offices, National Weather Services, and any organization
that needs to translate their existing TAC-producing systems' output into
WMO/ICAO IWXXM XML without re-engineering their observation/forecast pipeline.

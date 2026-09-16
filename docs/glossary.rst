Glossary
=========

.. glossary::

   TAC
      Traditional Alphanumeric Code — the legacy plain-text encoding of
      aviation weather reports/forecasts/advisories defined by ICAO Annex 3.

   IWXXM
      ICAO Meteorological Information Exchange Model — the WMO/ICAO XML
      schema family that TAC products are being migrated to.

   AHL
      Abbreviated Heading Line — the WMO bulletin header
      (``TTAAii CCCC YYGGgg [BBB]``) prefixed to a TAC bulletin, identifying
      bulletin type, originating centre, and issue time.

   AIXM
      Aeronautical Information Exchange Model — used within IWXXM to
      describe aerodromes/airports.

   GML
      Geography Markup Language (OGC) — used to encode all spatial geometry
      (points, surfaces) in IWXXM documents.

   Bulletin
      A GIFTs :class:`~gifts.common.bulletin.Bulletin` object: a list-like
      container of one or more encoded IWXXM XML reports, plus the ability
      to write a ``<MeteorologicalBulletin>`` wrapper document.

   AMHS
      Aeronautical Message Handling System — the network over which
      ``<MeteorologicalBulletin>`` documents are typically transmitted (as
      gzip-compressed File Transfer Body Parts).

   CRUX
      NCAR's Java-based XML schema/Schematron validator, used by the
      ``validation/`` tooling to check generated IWXXM documents.

   TPG
      Toy Parser Generator — the (bundled, LGPL) recursive-descent parser
      generator library used to implement every GIFTs TAC decoder.

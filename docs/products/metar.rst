METAR / SPECI
==============

Module: :mod:`gifts.METAR` (encoder orchestration),
:mod:`gifts.metarDecoder` (TAC → dict),
:mod:`gifts.metarEncoder` (dict → IWXXM).

Recognized WMO AHL
--------------------

.. code-block:: text

   S(A|P)[A-Z]{2}\d{2}\s+[A-Z]{4}\s+\d{6}(\s+[ACR]{2}[A-Z])?

(bulletin type ``T1T2 = "L"``, per WMO Manual 386)

Recognized TAC form
---------------------

.. code-block:: text

   ^(?:METAR|SPECI)\s+(?:COR\s+)?[A-Z][A-Z0-9]{3}\s.+?=

Example: ``METAR KORD 121856Z 09014KT 10SM FEW250 23/14 A2990=``

Usage
------

.. code-block:: python

   import gifts.METAR

   # geoLocationsDB: any object exposing .get(icaoID) -> "name|iata|alternate|lat lon elev"
   encoder = gifts.METAR.Encoder(geoLocationsDB)
   bulletin = encoder.encode(raw_bulletin_text, receiptTime='20240912T18:56:00Z')
   print(bulletin)
   bulletin.write(compress=True)

Decoded fields (``metarDecoder.Annex3``)
------------------------------------------

The TPG-grammar-based ``Annex3`` parser returns a dict with keys such as
``type`` (METAR/SPECI), ``ident``, ``itime``, ``wind``, ``vsby``, ``rvr``,
``pcp``, ``obv``, ``vcnty``, ``sky``, ``temps``, ``altimeter``, ``rewx``,
``windshear``, ``seastate``, ``rwystate``, and trend groups. On parse
failure the dict instead contains ``err_msg`` and the offending TAC is
skipped by the base :class:`~gifts.common.Encoder.Encoder`.

Encoded output (``metarEncoder.Annex3``)
------------------------------------------

- Root element: ``iwxxm:METAR`` (or ``iwxxm:SPECI``), namespace
  ``http://icao.int/iwxxm/2025-2``.
- ``xsi:schemaLocation`` points at
  ``https://schemas.wmo.int/iwxxm/2025-2RC1/iwxxm.xsd``.
- ``preamble()`` builds the root element and its report-level attributes
  (``reportStatus``, ``automatedStation``, etc.).
- ``observation()`` encodes wind, visibility, weather, clouds, temperature,
  and altimeter groups.
- ``forecasts()`` encodes any METAR trend forecast (BECMG/TEMPO) groups.
- Weather/cloud/recent-weather codes are resolved to WMO code-registry URNs
  via ``xmlUtilities.parseCodeRegistryTables`` (see :doc:`../data_mappings`).

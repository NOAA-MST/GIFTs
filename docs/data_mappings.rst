Data & Code Mappings
=====================

This page documents every place where GIFTs maps external reference data
(codes, coordinates, schemas) onto elements of the generated IWXXM XML.

WMO RDF code registries → xlink URNs
--------------------------------------

Location: :file:`gifts/data/*.rdf` (packaged via :file:`MANIFEST.in`).
Loaded by: :func:`gifts.common.xmlUtilities.parseCodeRegistryTables`.

.. list-table::
   :header-rows: 1

   * - RDF file
     - WMO code registry
     - Used for
   * - ``codes.wmo.int-49-2-AerodromePresentOrForecastWeather.rdf``
     - AerodromePresentOrForecastWeather
     - METAR/TAF present/forecast weather phenomena (RA, SN, FG, TS, …)
   * - ``codes.wmo.int-49-2-AerodromeRecentWeather.rdf``
     - AerodromeRecentWeather
     - METAR recent weather (``RE`` prefixed codes)
   * - ``codes.wmo.int-49-2-CloudAmountReportedAtAerodrome.rdf``
     - CloudAmountReportedAtAerodrome
     - Cloud cover amounts (SKC, FEW, SCT, BKN, OVC)
   * - ``codes.wmo.int-49-2-SigConvectiveCloudType.rdf``
     - SigConvectiveCloudType
     - Significant convective cloud type (CB, TCU)
   * - ``codes.wmo.int-49-2-SpaceWxLocation.rdf``
     - SpaceWxLocation
     - Space Weather Advisory affected-region codes
   * - ``codes.wmo.int-49-2-SpaceWxPhenomena.rdf``
     - SpaceWxPhenomena
     - Space Weather Advisory phenomena (RADIATION, GNSS, HF COM, SAT COM)
   * - ``codes.wmo.int-bufr4-codeflag-0-20-086.rdf``
     - BUFR 0-20-086
     - Runway deposit codes
   * - ``codes.wmo.int-bufr4-codeflag-0-20-087.rdf``
     - BUFR 0-20-087
     - Runway contamination extent codes
   * - ``codes.wmo.int-bufr4-codeflag-0-20-089.rdf``
     - BUFR 0-20-089
     - Runway friction coefficient / braking action codes
   * - ``codes.wmo.int-bufr4-codeflag-0-22-061.rdf``
     - BUFR 0-22-061
     - Sea-state/sea-surface condition codes
   * - ``codes.wmo.int-common-nil.rdf``
     - common/nil
     - "Nil reason" codes (missing, inapplicable, unknown, …)

These files are copies of vocabularies published at
`codes.wmo.int <http://codes.wmo.int/>`_ (WMO's SKOS/RDF code registry). Each
is parsed at encoder run time into a nested dict of the shape
``{containerName: {tacCode: (uri, preferredLabel)}}``. The URI is emitted as
an ``xlink:href`` attribute on the relevant IWXXM element; the label is
optionally emitted as ``xlink:title`` depending on the ``TITLES`` bit-mask
settings in :file:`gifts/common/xmlConfig.py`.

Because these are cached snapshots, they should be periodically refreshed
from codes.wmo.int if WMO publishes updates to the underlying registries.

Aerodrome geo-location database
----------------------------------

Location: :file:`gifts/database/aerodromes.tbl` (sample flat file) built by
:file:`gifts/database/create_pickle_db.py` into a pickled Python dict
(:file:`aerodromes.db`).

Flat-file schema (``|``-delimited):

.. list-table::
   :header-rows: 1

   * - Field
     - Format
     - Required?
   * - ICAO identifier
     - ``[A-Z]{4}``
     - Yes
   * - IATA identifier
     - ``[A-Z]{3}``
     - No
   * - Alternate identifier
     - ``[A-Z0-9]{3,6}``
     - No
   * - Full aerodrome name
     - up to 60 chars
     - No
   * - Latitude
     - ``[-]?\d{1,2}\.\d{0,5}`` degrees, WGS84 (south negative)
     - Yes
   * - Longitude
     - ``[-]?\d{1,3}\.\d{0,5}`` degrees, WGS84 (west negative)
     - Yes
   * - Elevation
     - metres above MSL
     - Yes

**Data flow**: the METAR/TAF decoder extracts the ICAO identifier from the
TAC → the product ``Encoder`` calls ``geoLocationsDB.get(icaoID)``, which
must return the string
``"name|iata|alternate|lat lon elevation"`` → this is split and merged into
the decoded TAC dict under the ``ident`` key → :class:`gifts.common.Common.Base`
uses it to build the ``<iwxxm:aerodrome><aixm:AirportHeliport>`` element,
including the ``ARP`` (Aerodrome Reference Point) position in
``EPSG:4326`` (WGS84) and, if ``xmlConfig.useElevation`` is ``True``, the
elevation with the configured vertical datum and unit of measure.

Any object implementing ``.get(icaoID, default)`` in this string format can
be substituted for the pickled dict (e.g. a real database client), which is
the intended extension point for production deployments.

xmlConfig.py — site/schema configuration
-------------------------------------------

:file:`gifts/common/xmlConfig.py` centralizes values referenced throughout
the encoders:

.. list-table::
   :header-rows: 1

   * - Setting
     - Purpose
   * - ``TRANSLATOR``
     - If ``True``, marks output as a translation on behalf of another
       office and adds translation metadata (translating centre name,
       reception time).
   * - ``_iwxxm`` / ``_release``
     - IWXXM version (``2025-2``) and schema release (``2025-2RC1``) used to
       build ``IWXXM_URI`` (``http://icao.int/iwxxm/2025-2``) and
       ``IWXXM_URL`` (schema location URL at schemas.wmo.int).
   * - ``CodesFilePath``
     - Directory searched for the WMO RDF code registry files
       (``./gifts/data/``).
   * - ``useElevation`` / ``verticalDatum`` / ``elevationUOM``
     - Whether to emit aerodrome elevation, which vertical datum
       (``EGM_96``/``AHD``/``NAVD88``) applies, and the unit of measure
       (``FT``/``M``).
   * - ``TITLES``
     - Bit-mask controlling whether human-readable ``xlink:title``
       attributes accompany code ``xlink:href`` references (weather, cloud
       amount, cloud type, sea condition).
   * - ``Max_SectorVisibility_1`` / ``Max_SectorVisibility_2`` /
       ``RVR_MaximumDistance``
     - Thresholds governing visibility/runway-visual-range encoding.

External XML namespaces referenced by generated documents
-------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Prefix
     - Namespace URI
     - Standard
   * - ``iwxxm``
     - ``http://icao.int/iwxxm/2025-2``
     - ICAO/WMO IWXXM
   * - ``aixm``
     - ``http://www.aixm.aero/schema/5.1.1``
     - Aeronautical Information Exchange Model
   * - ``gml``
     - ``http://www.opengis.net/gml/3.2``
     - OGC Geography Markup Language
   * - ``xlink``
     - ``http://www.w3.org/1999/xlink``
     - W3C XLink
   * - ``xsi``
     - ``http://www.w3.org/2001/XMLSchema-instance``
     - W3C XML Schema Instance
   * - (bulletin wrapper)
     - ``http://def.wmo.int/collect/2014``
     - WMO Collect (``<MeteorologicalBulletin>``)

Spatial reference: all coordinates are encoded against
``http://www.opengis.net/def/crs/EPSG/0/4326`` (WGS84), ``axisLabels="Lat
Long"``, ``srsDimension="2"``.

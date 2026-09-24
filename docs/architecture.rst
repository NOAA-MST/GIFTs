Architecture
=============

Pipeline overview
------------------

Every product follows the same pipeline, orchestrated by
:class:`gifts.common.Encoder.Encoder` (the base class every product-specific
``Encoder`` inherits from):

.. code-block:: text

   Raw bulletin text (WMO AHL line + one or more TAC forms)
        |
        v
   [1] WMO AHL regex match  --------------> aaii, cccc, yygg, bbb, tt
        |
        v
   [2] Per-product TAC-form regex extracts each individual TAC message
        |
        v
   [3] Decoder (TPG grammar parser) -------> Python dict, or dict with 'err_msg'
        |
        v
   [4] geoLocationsDB.get(icaoID) ---------> aerodrome name/IATA/lat/lon/elev
        |            (METAR & TAF only)
        v
   [5] Encoder (dict -> XML) --------------> iwxxm:* ElementTree.Element
        |     - loads WMO RDF code registries (data/*.rdf) to map TAC codes to URNs
        v
   [6] Bulletin container collects one Element per decoded TAC
        |
        v
   Bulletin.write() / str(bulletin) -------> <MeteorologicalBulletin> XML file
                                              (optionally gzip-compressed)

Key classes
------------

``gifts.common.Encoder.Encoder``
   Base class. Public method ``encode(text, receiptTime=None, **attrs) ->
   Bulletin``. Extracts the AHL line via ``self.re_AHL``, iterates over TAC
   forms found by ``self.re_TAC``, calls ``self.decoder(tac)``, optionally
   resolves aerodrome metadata via ``self.geoLocationsDB``, calls
   ``self.encoder(decodedTAC, tac)``, and appends the resulting XML element
   to a :class:`~gifts.common.bulletin.Bulletin`. Decode errors are logged
   and that TAC is skipped without aborting the whole bulletin.

``gifts.common.bulletin.Bulletin``
   List-like container of IWXXM XML :class:`~xml.etree.ElementTree.Element`
   objects (one per decoded report). Supports ``len()``, indexing, ``+``
   (combining two bulletins), ``str()`` (pretty-printed XML), and
   ``write(compress=False)`` which wraps the collected reports in a
   ``<MeteorologicalBulletin>`` document per the WMO Collect schema and
   writes it to disk (gzip-compressed if requested).

``gifts.common.Common.Base``
   Shared XML-building utilities used by every product encoder, notably
   ``aerodrome(parent_elem, token)`` which builds the
   ``<iwxxm:aerodrome><aixm:AirportHeliport>`` fragment (ICAO/IATA
   identifiers, name, ARP position in WGS84).

``gifts.common.xmlUtilities``
   ``parseCodeRegistryTables(srcDirectory, neededCodes, preferredLanguage='en')``
   loads WMO RDF code list files into ``{container: {code: (uri, label)}}``
   dictionaries used to resolve ``xlink:href``/``xlink:title`` attributes.
   Also provides compass-point-to-degree conversion and date/time helpers.

``gifts.common.tpg``
   A bundled copy of TPG (Toy Parser Generator) v3.2.4, an LGPL parser
   generator. Every decoder is implemented as a ``tpg.Parser`` subclass whose
   grammar (lexer tokens + BNF-like production rules with inline Python
   semantic actions) is embedded directly in the class docstring.

Why TPG?
---------

TAC forms are line-oriented, densely-coded, whitespace-delimited grammars
(e.g. ``09014KT`` for wind) that are naturally expressed as a small formal
grammar rather than ad-hoc regular expressions. TPG lets each decoder define
its lexer tokens and production rules together with the Python code that
builds the resulting dictionary, keeping the grammar and the semantic action
next to each other in one class.

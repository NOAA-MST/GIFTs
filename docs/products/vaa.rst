Volcanic Ash Advisory (VAA)
==============================

Module: :mod:`gifts.VAA`, :mod:`gifts.vaaDecoder`, :mod:`gifts.vaaEncoder`.

No geo-location database is required for this product.

Recognized WMO AHL
--------------------

.. code-block:: text

   FV\w{2}\d{2}\s+[A-Z]{4}\s+\d{6}(\s+[ACR]{2}[A-Z])?

(bulletin type ``T1T2 = "LU"``)

Recognized TAC form
---------------------

.. code-block:: text

   ^VA ADVISORY.+

Usage
------

.. code-block:: python

   import gifts.VAA

   encoder = gifts.VAA.Encoder()
   bulletin = encoder.encode(raw_bulletin_text)

Decoding notes (``vaaDecoder.Decoder``)
------------------------------------------

Extracts volcano/eruption details, observed and forecast ash-cloud
locations (lat/lon pairs, box areas, movement vectors), and vertical extent.
Raises :class:`~gifts.vaaDecoder.MissingAirSpaceWinds` internally when wind
information required for the ash-cloud forecast is absent.

Encoding notes (``vaaEncoder.Encoder``)
------------------------------------------

Output root: ``VolcanicAshAdvisory``, encoding the observed and forecast
ash-cloud geometries as GML surfaces/points per forecast hour.

Tropical Cyclone Advisory (TCA)
=================================

Module: :mod:`gifts.TCA`, :mod:`gifts.tcaDecoder`, :mod:`gifts.tcaEncoder`.

No geo-location database is required for this product.

Recognized WMO AHL
--------------------

.. code-block:: text

   FK\w{2}\d{2}\s+[A-Z]{4}\s+\d{6}(\s+[ACR]{2}[A-Z])?

(bulletin type ``T1T2 = "LK"``)

Recognized TAC form
---------------------

.. code-block:: text

   ^TC ADVISORY.+

Usage
------

.. code-block:: python

   import gifts.TCA

   encoder = gifts.TCA.Encoder()
   bulletin = encoder.encode(raw_bulletin_text)

Decoding notes (``tcaDecoder.Decoder``)
------------------------------------------

Extracts date/time group, issuing centre, cyclone name, advisory number,
observed position/movement/intensity change/central pressure/max wind, and
forecast positions/winds at subsequent forecast hours.

Encoding notes (``tcaEncoder.Encoder``)
------------------------------------------

Output root: ``TropicalCycloneAdvisory``, containing the observed analysis
and each forecast period as separate members.

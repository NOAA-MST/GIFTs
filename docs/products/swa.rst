Space Weather Advisory (SWA)
==============================

Module: :mod:`gifts.SWA`, :mod:`gifts.swaDecoder`, :mod:`gifts.swaEncoder`.

No geo-location database is required for this product.

Recognized WMO AHL
--------------------

.. code-block:: text

   FN\w{2}\d{2}\s+[A-Z]{4}\s+\d{6}(\s+[ACR]{2}[A-Z])?

(bulletin type ``T1T2 = "LN"``)

Recognized TAC form
---------------------

.. code-block:: text

   ^SWX ADVISORY.+

Usage
------

.. code-block:: python

   import gifts.SWA

   encoder = gifts.SWA.Encoder()
   bulletin = encoder.encode(raw_bulletin_text)

Decoding notes (``swaDecoder.Decoder``)
------------------------------------------

Extracts date/time group, issuing centre, advisory number, affected
phenomena (``RADIATION``, ``GNSS``, ``HF COM``, ``SAT COM``), per-forecast-hour
observations/latitude bands/flight levels/locations, remarks, and the next
advisory time. Uses the `skyfield <https://rhodesmill.org/skyfield/>`_
library for astronomical calculations (e.g. day/night terminator) that
inform latitude-band phenomena.

Encoding notes (``swaEncoder.Encoder``)
------------------------------------------

- Output root: ``SpaceWeatherAdvisory`` (unprefixed IWXXM element).
- Attributes include ``permissibleUsage`` and ``reportStatus``; if
  ``xmlConfig.TRANSLATOR`` is enabled, translation metadata (translating
  centre, reception time) is added.
- Key methods: ``preamble()``, ``observations()``, ``postContent()``.

TAF
====

Module: :mod:`gifts.TAF` (encoder orchestration),
:mod:`gifts.tafDecoder` (TAC → dict),
:mod:`gifts.tafEncoder` (dict → IWXXM).

Recognized WMO AHL
--------------------

.. code-block:: text

   F(C|T)\w{2}\d{2}\s+[A-Z]{4}\s+\d{6}(\s+[ACR]{2}[A-Z])?

(bulletin type ``T1T2 = "L"``)

Recognized TAC form
---------------------

.. code-block:: text

   ^TAF(?:\s+(?:AMD|COR|CC[A-Z]|RTD))?\s+[A-Z]{4}.+?=

Example: ``TAF KORD 121720Z 1218/1324 09012KT P6SM FEW250``

Usage
------

.. code-block:: python

   import gifts.TAF

   encoder = gifts.TAF.Encoder(geoLocationsDB)
   bulletin = encoder.encode(raw_bulletin_text)

Decoding notes (``tafDecoder.Decoder``)
------------------------------------------

Returns validity period, forecast change groups (``BECMG``, ``TEMPO``,
``PROB30``/``PROB40``), and the same core weather elements as METAR. Raises
:class:`~gifts.tafDecoder.CAVOKError` internally when a mandatory
visibility/sky-condition group is missing alongside ``CAVOK``.

Encoding notes (``tafEncoder.Encoder``)
------------------------------------------

- Root element: ``iwxxm:TAF``.
- ``reportStatus`` reflects ``AMENDMENT``/``CORRECTION``/``NORMAL`` derived
  from the ``bbb`` AHL field or ``AMD``/``COR`` TAC keywords; NIL'd and
  cancelled TAFs are represented distinctly.
- Change indicators are mapped: ``BECMG`` → ``BECOMING``, ``TEMPO`` →
  ``TEMPORARY_FLUCTUATIONS``, with ``PROB30``/``PROB40`` encoded as
  probability attributes on the relevant forecast conditions.

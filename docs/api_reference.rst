API Reference
==============

This page is generated from source docstrings via ``sphinx.ext.autodoc``.
Modules that require optional/site-specific setup (e.g. a real
``geoLocationsDB``) are still importable and documented, but their runtime
behavior depends on caller-supplied configuration described in
:doc:`data_mappings`.

Top-level product encoders
------------------------------

.. automodule:: gifts.METAR
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: gifts.TAF
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: gifts.SWA
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: gifts.TCA
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: gifts.VAA
   :members:
   :undoc-members:
   :show-inheritance:

Decoders
---------

.. note::
   Decoder classes embed their TPG grammar (lexer tokens and BNF-like
   production rules) directly in the class docstring. That grammar text is
   not valid reStructuredText, so it is intentionally *not* rendered here —
   see the source files directly, or the per-product pages under
   :doc:`products/index` for a plain-language summary of each grammar.

.. automodule:: gifts.metarDecoder
   :no-undoc-members:

.. automodule:: gifts.tafDecoder
   :no-undoc-members:

.. automodule:: gifts.swaDecoder
   :no-undoc-members:

.. automodule:: gifts.tcaDecoder
   :no-undoc-members:

.. automodule:: gifts.vaaDecoder
   :no-undoc-members:

Encoders
---------

.. automodule:: gifts.metarEncoder
   :members:
   :undoc-members:

.. automodule:: gifts.tafEncoder
   :members:
   :undoc-members:

.. automodule:: gifts.swaEncoder
   :members:
   :undoc-members:

.. automodule:: gifts.tcaEncoder
   :members:
   :undoc-members:

.. automodule:: gifts.vaaEncoder
   :members:
   :undoc-members:

Common infrastructure
------------------------

.. automodule:: gifts.common.Encoder
   :members:
   :undoc-members:

.. automodule:: gifts.common.bulletin
   :members:
   :undoc-members:

.. automodule:: gifts.common.Common
   :members:
   :undoc-members:

.. automodule:: gifts.common.xmlConfig
   :members:

.. automodule:: gifts.common.xmlUtilities
   :members:
   :undoc-members:

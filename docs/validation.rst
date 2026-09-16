IWXXM Validation
=================

GIFTs produces IWXXM XML but does not validate it. The :file:`validation/`
subdirectory provides a separate, optional toolchain to check that
generated documents are well-formed XML and comply with the IWXXM XSD
schemas and Schematron ("business rule") constraints before dissemination.

Components
-----------

- **``iwxxmValidator.py``** — main entry point. Given an IWXXM version and a
  directory of XML files, it:

  1. Fetches (or uses cached) IWXXM-version-specific XSD schemas and
     Schematron rules from WMO, if not already present locally.
  2. Invokes the bundled Java **CRUX** utility
     (:file:`validation/bin/crux-1.3-all.jar`,
     `NCAR/crux <https://github.com/NCAR/crux>`_) to validate each XML file
     against the schemas and Schematron rules.
  3. Optionally checks GML id/reference integrity.
  4. Reports validation results/errors.

- **``checkGMLReferences.py``** — verifies that every ``xlink:href="#..."``
  reference to a local GML ``gml:id`` actually resolves within the document.
- **``codeListsToSchematron.py``** — converts WMO code list RDF into
  Schematron rules for validation.

Prerequisites
--------------

- Python 3.9+, with ``lxml`` and ``requests`` installed.
- A Java runtime capable of executing the bundled CRUX jar.

Cached external schemas
--------------------------

:file:`validation/externalSchemas/` contains local copies of schemas that
should be periodically refreshed:

- ``aero/aixm`` 5.1 and 5.1.1 (plus the ``AIXM_WX`` profiles)
- ``org/w3c`` (XML namespace/XSD)
- ``schemas.opengis.net`` — GML 3.2.1, ISO 19139, OM 2.0, sampling /
  samplingSpatial 2.0, SWE Common 2.0
- ``schemas.wmo.int`` — collect 1.1/1.2, metce 1.0/1.1/1.2, opm 1.0/1.1/1.2,
  saf 1.0/1.1 (with Schematron ``rule`` subfolders)

Usage
------

See :file:`validation/README.md` for exact command-line arguments
(``version``, ``directory``, fetch/``useInternet``/``keep`` flags,
``noGMLChecks``). Typical flow: generate IWXXM XML with GIFTs, point
``iwxxmValidator.py`` at the output directory with the matching IWXXM
version, and review the reported schema/schematron errors before
dissemination.

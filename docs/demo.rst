Demo Programs
==============

The :file:`demo/` directory (outside the installable package) illustrates
end-to-end use of GIFTs.

``demo1.py`` — Tkinter GUI translator
-----------------------------------------

A small Tkinter application that:

1. Lets you browse for a ``.txt`` file containing one or more TAC bulletins
   (WMO AHL line + TAC form(s)).
2. Determines the product type by matching the AHL line against each
   product encoder's ``re_AHL`` pattern (METAR/SPECI, TAF, SWA, TCA, VAA).
3. Loads a prebuilt aerodrome pickle database (``aerodromes.db`` or
   ``aerodromes.win.db``) for METAR/TAF aerodrome lookups.
4. Displays decode/encode warnings and errors in a scrolled text pane via a
   custom ``TextHandler`` logging handler.
5. Writes the resulting IWXXM ``Bulletin`` to a user-specified output file.

Sample TAC input files shipped alongside it:

- ``metars.txt`` — METAR/SPECI reports
- ``tafs.txt`` — TAF reports
- ``tca.txt`` — Tropical Cyclone Advisory
- ``vaa.txt`` — Volcanic Ash Advisory

``iwxxmd.py`` / ``iwxxmd.cfg``
---------------------------------

A configuration-file-driven skeleton for a daemon/service mode (product
type, input/output/log directories, whether to delete input after
processing, whether input already contains a WMO AHL line). See
:file:`demo/iwxxmd.cfg` for the ``[internals]`` and ``[directories]``
sections.

See :file:`demo/README.md` in the repository for step-by-step usage
instructions.

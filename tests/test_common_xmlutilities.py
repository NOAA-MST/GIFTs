import math
import os

import pytest

from gifts.common import xmlUtilities as deu


RDF_TEMPLATE = '''<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:skos="http://www.w3.org/2004/02/skos/core#"
         xmlns:xml="http://www.w3.org/XML/1998/namespace">
  <skos:Concept rdf:about="http://codes.wmo.int/test/{key}">
    {labels}
  </skos:Concept>
</rdf:RDF>
'''


def _write_rdf(path, key, labels):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(RDF_TEMPLATE.format(key=key, labels=labels))


def test_parse_code_registry_tables_adds_nil_and_falls_back_languages(tmp_path):
    weather_file = os.path.join(tmp_path, 'AerodromePresentOrForecastWeather.rdf')
    nil_file = os.path.join(tmp_path, 'nil.rdf')

    _write_rdf(
        weather_file,
        'RA',
        '<rdfs:label xml:lang="en">Rain</rdfs:label><rdfs:label xml:lang="fr">Pluie</rdfs:label>',
    )
    _write_rdf(nil_file, 'missing', '<rdfs:label>Missing-No-Lang</rdfs:label>')

    needed_codes = ['AerodromePresentOrForecastWeather']
    codes = deu.parseCodeRegistryTables(str(tmp_path), needed_codes, preferredLanguage='de')

    assert 'nil' in needed_codes
    assert codes['AerodromePresentOrForecastWeather']['RA'][1] == 'Rain'
    assert codes['nil']['missing'][1] == ''


def test_fix_date_previous_month(monkeypatch):
    monkeypatch.setattr(deu.time, 'time', lambda: 1_000_000)
    monkeypatch.setattr(deu.time, 'mktime', lambda _t: 1_000_000 + 4 * 86400)

    tms = [2026, 5, 20, 10, 0, 0, 0, 0, -1]
    deu.fix_date(tms)

    assert tms[1] == 4


def test_fix_date_next_month_and_year(monkeypatch):
    monkeypatch.setattr(deu.time, 'time', lambda: 1_000_000)
    monkeypatch.setattr(deu.time, 'mktime', lambda _t: 1_000_000 - 26 * 86400)

    tms = [2026, 12, 20, 10, 0, 0, 0, 0, -1]
    deu.fix_date(tms)

    assert tms[1] == 1
    assert tms[0] == 2027


def test_is_a_number_and_get_uuid(monkeypatch):
    assert deu.is_a_number('-12.5') is True
    assert deu.is_a_number('abc') is False

    monkeypatch.setattr(deu.uuid, 'uuid4', lambda: 'abc123')
    assert deu.getUUID() == 'uuid.abc123'
    assert deu.getUUID(prefix='id:') == 'id:abc123'


def test_compute_lat_lon_wraps_longitude():
    wrapped_east = deu.computeLatLon(0.0, 179.9, 90, 20)
    wrapped_west = deu.computeLatLon(0.0, -179.9, 270, 20)

    east_lon = float(wrapped_east.split()[1])
    west_lon = float(wrapped_west.split()[1])
    assert -180.0 <= east_lon <= 180.0
    assert -180.0 <= west_lon <= 180.0


def test_check_visibility_thresholds_and_units():
    assert deu.checkVisibility(749) == 700
    assert deu.checkVisibility(3200) == 3200
    assert deu.checkVisibility(9800) == 9000
    assert deu.checkVisibility(10050) == 10000

    one_mile = deu.checkVisibility('1', uom='[mi_i]')
    assert one_mile == '1600'


def test_check_rvr_thresholds_and_units():
    assert deu.checkRVR(399) == 375
    assert deu.checkRVR(800) == 800
    assert deu.checkRVR(1001) == 1000

    thousand_feet = deu.checkRVR('1000', uom='[ft_i]')
    assert thousand_feet == '300'


def test_compute_area_and_orientation():
    with pytest.raises(ValueError):
        deu.computeArea([(0, 0), (1, 1)])

    polygon_cw = [(0, 0), (0, 1), (1, 1), (1, 0)]
    area = deu.computeArea(polygon_cw[:])
    assert math.isfinite(area)
    assert deu.isCCW(polygon_cw[:]) is True

    polygon_ccw = [(0, 0), (1, 0), (1, 1), (0, 1)]
    assert deu.isCCW(polygon_ccw[:]) is False

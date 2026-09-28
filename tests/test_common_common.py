import xml.etree.ElementTree as ET

from gifts.common.Common import Base
from gifts.common import xmlConfig as des


def _child_tags(elem):
    return [child.tag for child in elem]


def test_aerodrome_with_none_token_creates_empty_container():
    base = Base()
    parent = ET.Element('root')

    base.aerodrome(parent, None)

    assert len(parent) == 1
    assert parent[0].tag == 'iwxxm:aerodrome'
    assert len(parent[0]) == 0


def test_aerodrome_populates_expected_fields(monkeypatch):
    monkeypatch.setattr('gifts.common.xmlUtilities.getUUID', lambda: 'uuid.fixed')
    monkeypatch.setattr(des, 'useElevation', True)
    monkeypatch.setattr(des, 'srsDimension', '2')

    token = {
        'str': 'KJFK',
        'alternate': 'AB12',
        'name': 'John F Kennedy',
        'iataID': 'JFK',
        'position': '40.639 -73.778 13',
    }

    base = Base()
    parent = ET.Element('root')
    base.aerodrome(parent, token)

    node = parent.find('iwxxm:aerodrome')
    assert node is not None

    airport = node.find('aixm:AirportHeliport')
    assert airport is not None
    assert airport.get('gml:id') == 'uuid.fixed'

    time_slice = airport.find('aixm:timeSlice').find('aixm:AirportHeliportTimeSlice')
    assert time_slice.find('aixm:interpretation').text == 'SNAPSHOT'
    assert time_slice.find('aixm:designator').text == 'AB12'
    assert time_slice.find('aixm:name').text == 'John F Kennedy'
    assert time_slice.find('aixm:locationIndicatorICAO').text == 'KJFK'
    assert time_slice.find('aixm:designatorIATA').text == 'JFK'

    pos = time_slice.find('aixm:ARP').find('aixm:ElevatedPoint').find('gml:pos')
    assert pos.text == '40.639 -73.778'

    elevated_point = time_slice.find('aixm:ARP').find('aixm:ElevatedPoint')
    assert elevated_point.find('aixm:elevation').text == '13'
    assert elevated_point.find('aixm:verticalDatum').text == des.verticalDatum


def test_aerodrome_ignores_invalid_ids_and_missing_elevation(monkeypatch):
    monkeypatch.setattr('gifts.common.xmlUtilities.getUUID', lambda: 'uuid.fixed')
    monkeypatch.setattr(des, 'useElevation', True)

    token = {
        'str': '12AB',
        'alternate': 'TOO-LONG',
        'iataID': 'A1',
        'position': '10.0 20.0',
    }

    base = Base()
    parent = ET.Element('root')
    base.aerodrome(parent, token)

    time_slice = parent.find('.//aixm:AirportHeliportTimeSlice')
    tags = _child_tags(time_slice)

    assert 'aixm:designator' not in tags
    assert 'aixm:locationIndicatorICAO' not in tags
    assert 'aixm:designatorIATA' not in tags

    elevated = parent.find('.//aixm:ElevatedPoint')
    assert elevated.find('aixm:elevation') is None
    assert elevated.find('aixm:verticalDatum') is None

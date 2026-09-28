import logging
import re
import xml.etree.ElementTree as ET

import pytest

from gifts.common.Encoder import Encoder
from gifts.common import xmlConfig as des


class DummyEncoder(Encoder):
    def __init__(self):
        super().__init__()
        self.re_AHL = re.compile(r'(?P<aaii>\d{2}) (?P<cccc>[A-Z]{4}) (?P<yygg>\d{6})(?P<bbb> [A-Z]{3})?')
        self.re_TAC = re.compile(r'TAC:([^\n=]+)')
        self.T1T2 = 'L'
        self.seen = []

    def decoder(self, tac):
        tac = tac.strip()
        payload = {
            'bbb': '',
            'ident': {'str': 'KJFK'},
            'translationTime': '2026-01-01T00:00:00Z',
            'payload': tac,
        }
        if tac == 'ERR':
            payload['err_msg'] = 'bad tac'
        return payload

    def encoder(self, decoded_tac, tac):
        if tac.strip() == 'SYNTAX':
            raise SyntaxError('bad syntax')
        self.seen.append(decoded_tac.copy())
        return ET.Element('iwxxm:Dummy')


class BadGeoDB:
    def get(self, *_args, **_kwargs):
        raise KeyError('missing')


def test_encode_returns_empty_when_no_ahl():
    encoder = DummyEncoder()

    collection = encoder.encode('no header here')

    assert len(collection) == 0


def test_encode_translator_mode_and_default_bbb(monkeypatch):
    monkeypatch.setattr(des, 'TRANSLATOR', True)

    encoder = DummyEncoder()
    text = '12 KJFK 281200\nTAC:OK1\nTAC:OK2='
    collection = encoder.encode(text, receiptTime='2026-09-28T00:00:00Z')

    assert len(collection) == 2
    assert all(item['bbb'] == '' for item in encoder.seen)
    assert all(item['translatedBulletinID'] == '12KJFK281200' for item in encoder.seen)
    assert all(item['translatedBulletinReceptionTime'] == '2026-09-28T00:00:00Z' for item in encoder.seen)


def test_encode_logs_and_skips_decode_errors_when_not_translator(caplog, monkeypatch):
    monkeypatch.setattr(des, 'TRANSLATOR', False)

    encoder = DummyEncoder()
    with caplog.at_level(logging.WARNING):
        collection = encoder.encode('12 KJFK 281200\nTAC:ERR=')

    assert len(collection) == 0
    assert 'Will not create IWXXM document for KJFK' in caplog.text


def test_encode_geo_db_enrichment_and_zero_position_warning(caplog, monkeypatch):
    monkeypatch.setattr(des, 'TRANSLATOR', True)

    encoder = DummyEncoder()
    encoder.geoLocationsDB = {'KJFK': 'Airport Name|JFK|ALT01|0.0 0.0 0'}
    with caplog.at_level(logging.WARNING):
        collection = encoder.encode('12 KJFK 281200\nTAC:OK1=')

    assert len(collection) == 1
    seen = encoder.seen[0]['ident']
    assert seen['name'] == 'Airport Name'
    assert seen['iataID'] == 'JFK'
    assert seen['alternate'] == 'ALT01'
    assert seen['position'] == '0.0 0.0 0'
    assert 'not found in geoLocationsDB' in caplog.text


def test_encode_geo_db_key_error_skips_tac(monkeypatch):
    monkeypatch.setattr(des, 'TRANSLATOR', True)

    encoder = DummyEncoder()
    encoder.geoLocationsDB = BadGeoDB()

    collection = encoder.encode('12 KJFK 281200\nTAC:OK1=')

    assert len(collection) == 0


def test_encode_handles_encoder_syntax_errors(monkeypatch):
    monkeypatch.setattr(des, 'TRANSLATOR', True)

    encoder = DummyEncoder()
    collection = encoder.encode('12 KJFK 281200\nTAC:SYNTAX=')

    assert len(collection) == 0

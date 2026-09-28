import io
import xml.etree.ElementTree as ET

import pytest

from gifts.common import bulletin


def _build_bulletin_with_child():
    b = bulletin.Bulletin()
    b.append(ET.Element('iwxxm:Test'))
    b.set_bulletinIdentifier(tt='LK', aaii='NT22', cccc='KNHC', yygg='151436', bbb='')
    return b


def test_str_returns_xml_and_resets_internal_bulletin():
    b = _build_bulletin_with_child()

    xml_text = str(b)

    assert '<MeteorologicalBulletin' in xml_text
    assert b.bulletin is None


def test_export_rejects_bad_bulletin_identifier():
    b = bulletin.Bulletin()
    b.append(ET.Element('iwxxm:Test'))
    b._bulletinId = 'not-valid-id'

    with pytest.raises(SyntaxError):
        b.export()


def test_write_raises_for_unsupported_object_type():
    b = _build_bulletin_with_child()

    with pytest.raises(IOError):
        b.write(obj=123)


def test_iswriteable_recognizes_binary_writable_objects():
    b = bulletin.Bulletin()
    sink = io.BytesIO()
    sink.mode = 'wb'

    assert b._iswriteable(sink) is True


def test_write_compress_requires_gzip(monkeypatch):
    b = _build_bulletin_with_child()
    monkeypatch.delattr(bulletin, 'gzip', raising=False)

    with pytest.raises(SystemError):
        b.write(compress=True)

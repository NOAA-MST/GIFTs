import io
import os
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


def test_add_and_append_behavior_and_kind_validation():
    left = bulletin.Bulletin()
    right = bulletin.Bulletin()
    left.append(ET.Element('iwxxm:Left'))
    right.append(ET.Element('iwxxm:Right'))

    with pytest.raises(SyntaxError):
        left + right

    one = bulletin.Bulletin()
    two = bulletin.Bulletin()
    one.append(ET.Element('iwxxm:Test'))
    two.append(ET.Element('iwxxm:Test'))
    combined = one + two
    assert len(combined) == 2

    popped = combined.pop()
    assert popped.tag == 'iwxxm:Test'
    assert combined.what_kind() == 'iwxxm:Test'

    with pytest.raises(SyntaxError):
        one.append(ET.Element('iwxxm:Other'))


def test_add_empty_bulletins_raises():
    with pytest.raises(SyntaxError):
        bulletin.Bulletin() + bulletin.Bulletin()


def test_export_raises_for_empty_and_missing_identifier():
    empty = bulletin.Bulletin()
    with pytest.raises(SyntaxError):
        empty.export()

    missing_id = bulletin.Bulletin()
    missing_id.append(ET.Element('iwxxm:Test'))
    with pytest.raises(SyntaxError):
        missing_id.export()


def test_write_to_directory_and_header_extension(tmp_path):
    b = _build_bulletin_with_child()
    path = b.write(str(tmp_path), header=True)

    assert path.endswith('.txt')
    assert os.path.exists(path)
    with open(path, 'r', encoding='utf-8') as fh:
        assert fh.readline().startswith('LKNT22 KNHC 151436')


def test_write_to_current_directory_when_obj_is_none(tmp_path, monkeypatch):
    b = _build_bulletin_with_child()
    monkeypatch.chdir(tmp_path)
    path = b.write()

    assert os.path.exists(path)
    assert path.endswith('.xml')


def test_write_with_compression_creates_gzip_file(tmp_path):
    b = _build_bulletin_with_child()
    path = b.write(str(tmp_path), compress=True, header=True)

    assert path.endswith('.xml.gz')
    assert os.path.exists(path)


def test_write_falls_back_when_short_empty_elements_unsupported(monkeypatch):
    b = _build_bulletin_with_child()
    b.export()
    sink = io.BytesIO()
    sink.mode = 'wb'

    original = ET.ElementTree.write

    def flaky_write(self, file_or_filename, **kwargs):
        if 'short_empty_elements' in kwargs:
            raise TypeError('unsupported')
        return original(self, file_or_filename, **kwargs)

    monkeypatch.setattr(ET.ElementTree, 'write', flaky_write)
    b._write(sink, header=False, compress=False)
    assert sink.getvalue().startswith(b'<?xml version=')

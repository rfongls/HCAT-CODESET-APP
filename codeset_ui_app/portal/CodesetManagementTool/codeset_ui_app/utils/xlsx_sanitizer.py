from __future__ import annotations

import re
from io import BytesIO
from zipfile import ZipFile


def strip_invalid_font_families(xlsx_bytes: bytes) -> bytes:
    """Remove font family tags that exceed OpenXML limits.

    Older workbooks sometimes contain ``<family>`` elements with ``val``
    attributes greater than Excel's permitted range (0-14). ``openpyxl``
    raises ``ValueError`` when encountering these values. This helper strips
    any ``family`` elements from ``xl/sharedStrings.xml`` and ``xl/styles.xml``
    so the workbook can be parsed.
    """
    out = BytesIO()
    with ZipFile(BytesIO(xlsx_bytes)) as zin, ZipFile(out, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename in ("xl/sharedStrings.xml", "xl/styles.xml"):
                data = re.sub(rb"<[^>]*family[^>]*/>", b"", data)
            zout.writestr(info, data)
    return out.getvalue()

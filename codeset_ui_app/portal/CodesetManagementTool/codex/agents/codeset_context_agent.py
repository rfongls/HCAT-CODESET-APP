from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

from ..validators.validate_codeset_tab_logic import validate_codeset_tab_logic, DEFAULT_DEFINITION


class CodesetContextAgent:
    """Simple reference agent that exposes spreadsheet rules and validation."""

    def __init__(self, definition_path: Path | None = None) -> None:
        self.definition_path = definition_path or DEFAULT_DEFINITION
        self._context = Path(self.definition_path).read_text()

    @property
    def context(self) -> str:
        """Return the raw markdown context."""
        return self._context

    def validate(self, workbook_path: str | Path) -> List[Dict[str, Any]]:
        """Validate a workbook using :func:`validate_codeset_tab_logic`."""
        return validate_codeset_tab_logic(workbook_path, self.definition_path)

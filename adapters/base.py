"""Editor adapter contract. Every editor (real or mock) implements apply_recipe."""
from pathlib import Path
from typing import Protocol


class EditorAdapter(Protocol):
    def apply_recipe(self, src: Path, dst: Path, recipe: dict) -> Path:
        """Write the edited image to dst and return dst. Raise ValueError on a bad recipe."""
        ...

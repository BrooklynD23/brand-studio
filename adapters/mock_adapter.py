"""Mock editor for demos and tests: copies the source and records the recipe."""
import json
from pathlib import Path


class MockAdapter:
    def apply_recipe(self, src: Path, dst: Path, recipe: dict) -> Path:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(Path(src).read_bytes())
        dst.with_suffix(dst.suffix + ".recipe.json").write_text(json.dumps(recipe))
        return dst

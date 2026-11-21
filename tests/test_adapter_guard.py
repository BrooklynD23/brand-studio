"""Bad recipes must fail loudly, not write a wrong image."""
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from adapters.pillow_adapter import PillowAdapter  # noqa: E402


def test_crop_outside_image_raises(tmp_path):
    src = tmp_path / "a.png"
    Image.new("RGB", (50, 50)).save(src)
    with pytest.raises(ValueError, match="outside image"):
        PillowAdapter().apply_recipe(src, tmp_path / "b.png", {"crop": [0, 0, 999, 10]})
    assert not (tmp_path / "b.png").exists()


def test_unknown_recipe_key_raises(tmp_path):
    src = tmp_path / "a.png"
    Image.new("RGB", (50, 50)).save(src)
    with pytest.raises(ValueError, match="unsupported"):
        PillowAdapter().apply_recipe(src, tmp_path / "b.png", {"sharpen": 2})

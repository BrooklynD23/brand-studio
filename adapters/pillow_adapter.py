"""Local editor: applies a JSON edit recipe with Pillow. No Adobe dependency.

Recipe keys (all optional): crop [left, top, right, bottom] in pixels,
brightness (1.0 = unchanged), saturation (1.0 = unchanged).
"""
from pathlib import Path

from PIL import Image, ImageEnhance

ALLOWED_KEYS = {"crop", "brightness", "saturation"}


class PillowAdapter:
    def apply_recipe(self, src: Path, dst: Path, recipe: dict) -> Path:
        unknown = set(recipe) - ALLOWED_KEYS
        if unknown:
            raise ValueError(f"unsupported recipe keys: {sorted(unknown)}")
        img = Image.open(src).convert("RGB")
        if "crop" in recipe:
            left, top, right, bottom = recipe["crop"]
            if not (0 <= left < right <= img.width and 0 <= top < bottom <= img.height):
                raise ValueError(f"crop {recipe['crop']} outside image {img.size}")
            img = img.crop((left, top, right, bottom))
        if "brightness" in recipe:
            img = ImageEnhance.Brightness(img).enhance(float(recipe["brightness"]))
        if "saturation" in recipe:
            img = ImageEnhance.Color(img).enhance(float(recipe["saturation"]))
        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst)
        return dst

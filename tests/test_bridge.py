"""One flow test: task -> atomic claim -> Pillow edit -> done. Plus double-claim guard."""
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapters.pillow_adapter import PillowAdapter  # noqa: E402
from bridge.tasks import claim_task, finish_task  # noqa: E402


def test_claim_edit_finish(tmp_path):
    (tmp_path / "tasks/inbox").mkdir(parents=True)
    (tmp_path / "tasks/claimed").mkdir(parents=True)
    (tmp_path / "tasks/done").mkdir(parents=True)
    src = tmp_path / "photo.png"
    Image.new("RGB", (200, 100), (120, 60, 30)).save(src)
    task = {"id": "T-001", "src": str(src), "dst": str(tmp_path / "out/photo.png"),
            "recipe": {"crop": [0, 0, 100, 50], "brightness": 1.2}}
    (tmp_path / "tasks/inbox/T-001.json").write_text(json.dumps(task))

    claimed = claim_task(tmp_path, "T-001.json")
    assert claimed["id"] == "T-001"
    assert claim_task(tmp_path, "T-001.json") is None  # second worker gets nothing

    out = PillowAdapter().apply_recipe(Path(claimed["src"]), Path(claimed["dst"]), claimed["recipe"])
    assert Image.open(out).size == (100, 50)

    done = finish_task(tmp_path, "T-001.json", {"output": str(out)})
    assert json.loads(done.read_text())["status"] == "done"
    assert not (tmp_path / "tasks/claimed/T-001.json").exists()

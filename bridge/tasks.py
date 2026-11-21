"""File-based task bridge. Agents drop JSON tasks in inbox/; a worker claims one by
atomic rename (inbox -> claimed), so two workers cannot take the same task."""
import json
import os
from pathlib import Path


def claim_task(root: Path, name: str) -> dict | None:
    """Claim tasks/inbox/<name>. Return the task dict, or None if another worker won."""
    src = root / "tasks" / "inbox" / name
    dst = root / "tasks" / "claimed" / name
    try:
        os.rename(src, dst)  # atomic on one filesystem; fails if src is gone
    except FileNotFoundError:
        return None
    return json.loads(dst.read_text())


def finish_task(root: Path, name: str, result: dict) -> Path:
    """Move a claimed task to done/ with its result and status."""
    claimed = root / "tasks" / "claimed" / name
    task = json.loads(claimed.read_text())
    task.update(status="done", result=result)
    done = root / "tasks" / "done" / name
    done.write_text(json.dumps(task, indent=2))
    claimed.unlink()
    return done

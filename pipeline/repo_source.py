"""
Resolve a repo source (local path OR git URL) to a local directory.

Git URLs are cloned into a stable location under ~/.code-to-spec/clones/ keyed
by host/owner/repo, so re-running the same URL reuses the clone (and keeps the
cross-run memory key stable) instead of re-downloading to a random temp dir.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

CLONES_DIR = Path("~/.code-to-spec/clones").expanduser()

_GIT_URL_RE = re.compile(
    r"""^(
        https?://[^\s]+         |   # https://host/owner/repo(.git)
        git@[^\s:]+:[^\s]+      |   # git@host:owner/repo.git
        ssh://[^\s]+            |   # ssh://...
        [^\s/]+/[^\s/]+\.git        # shorthand ending in .git
    )$""",
    re.VERBOSE,
)


def is_git_url(source: str) -> bool:
    s = source.strip()
    if _GIT_URL_RE.match(s):
        return True
    # github.com/owner/repo shorthand without scheme
    return bool(re.match(r"^(github\.com|gitlab\.com|bitbucket\.org)/[^\s]+/[^\s]+$", s))


def _clone_dir_name(url: str) -> str:
    """Derive a stable, filesystem-safe directory name from a git URL."""
    s = url.strip()
    s = re.sub(r"\.git$", "", s)
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^git@", "", s)
    s = re.sub(r"^ssh://", "", s)
    s = s.replace(":", "/")
    parts = [p for p in s.split("/") if p]
    return "__".join(parts[-3:]) if parts else "repo"


def _normalize_url(url: str) -> str:
    s = url.strip()
    if is_git_url(s) and not re.match(r"^(https?|git@|ssh)", s):
        # bare shorthand like github.com/owner/repo → https://
        return "https://" + s
    return s


def resolve_repo_source(source: str, log=print, force_fresh: bool = False) -> str:
    """Return a local directory path for the given source.

    Local existing dirs are returned as-is. Git URLs are cloned (shallow) into a
    stable directory and reused/updated on subsequent runs.
    """
    s = source.strip()

    local = Path(s).expanduser()
    if local.is_dir():
        return str(local.resolve())

    if not is_git_url(s):
        raise ValueError(
            f"'{source}' is neither an existing directory nor a recognised git URL."
        )

    url = _normalize_url(s)
    CLONES_DIR.mkdir(parents=True, exist_ok=True)
    dest = CLONES_DIR / _clone_dir_name(url)

    if dest.exists() and force_fresh:
        import shutil
        shutil.rmtree(dest, ignore_errors=True)

    if dest.exists() and (dest / ".git").exists():
        log(f"Updating existing clone: {dest}")
        subprocess.run(
            ["git", "-C", str(dest), "pull", "--ff-only", "--depth", "1"],
            capture_output=True, text=True,
        )  # best-effort; stale clone is still usable
        return str(dest)

    log(f"Cloning {url} → {dest}")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", url, str(dest)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git clone failed: {result.stderr.strip() or result.stdout.strip()}")
    return str(dest)

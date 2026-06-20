import hashlib

HASH_LEN = 12


def content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()[:HASH_LEN]


def fingerprint(fname: str, content: bytes) -> str:
    """`main.css` + content -> `main.<hash>.css`. Hash sits before the extension."""
    stem, dot, ext = fname.rpartition(".")
    if not dot:
        return f"{fname}.{content_hash(content)}"
    return f"{stem}.{content_hash(content)}.{ext}"


def split_fingerprint(fname: str) -> tuple[str, str] | None:
    """`main.<hash>.css` -> (`main.css`, `<hash>`); None when no hash segment present.

    The hash is always the segment right before the extension, so re-joining
    the rest recovers the on-disk name regardless of dots in the stem.
    """
    parts = fname.split(".")
    if len(parts) < 3:
        return None
    *stem, file_hash, ext = parts
    return f"{'.'.join(stem)}.{ext}", file_hash

import pytest

from j0suetm.domain import fingerprint


def test_content_hash_is_deterministic_hex_of_fixed_length() -> None:
    digest = fingerprint.content_hash(b"body{}")

    assert digest == fingerprint.content_hash(b"body{}")
    assert len(digest) == fingerprint.HASH_LEN
    assert all(c in "0123456789abcdef" for c in digest)


def test_content_hash_changes_with_content() -> None:
    assert fingerprint.content_hash(b"a") != fingerprint.content_hash(b"b")


def test_fingerprint_inserts_hash_before_extension() -> None:
    digest = fingerprint.content_hash(b"x")

    assert fingerprint.fingerprint("main.css", b"x") == f"main.{digest}.css"


def test_fingerprint_appends_hash_when_no_extension() -> None:
    digest = fingerprint.content_hash(b"x")

    assert fingerprint.fingerprint("LICENSE", b"x") == f"LICENSE.{digest}"


@pytest.mark.parametrize(
    ("fname", "expected"),
    [
        ("main.abc123abc123.css", ("main.css", "abc123abc123")),
        ("main.min.deadbeef0000.css", ("main.min.css", "deadbeef0000")),
    ],
)
def test_split_fingerprint_recovers_name_and_hash(
    fname: str, expected: tuple[str, str]
) -> None:
    assert fingerprint.split_fingerprint(fname) == expected


@pytest.mark.parametrize("fname", ["main.css", "main", ""])
def test_split_fingerprint_returns_none_without_hash_segment(fname: str) -> None:
    assert fingerprint.split_fingerprint(fname) is None


def test_split_is_inverse_of_fingerprint() -> None:
    content = b"body{color:red}"
    hashed = fingerprint.fingerprint("main.css", content)

    assert fingerprint.split_fingerprint(hashed) == (
        "main.css",
        fingerprint.content_hash(content),
    )

from pathlib import Path

from pytest_mock import MockerFixture

from j0suetm import infra
from j0suetm.services.inbound import fs_in


def _point_dir(mocker: MockerFixture, prop: str, path: Path) -> None:
    # styles_dir / scripts_dir are read-only properties on Config; patch the
    # class so the singleton resolves to a throwaway temp dir.
    mocker.patch.object(
        type(infra.global_cfg),
        prop,
        new_callable=mocker.PropertyMock,
        return_value=path,
    )


def test_get_style_reads_existing_file(mocker: MockerFixture, tmp_path: Path) -> None:
    styles = tmp_path / "styles"
    styles.mkdir()
    (styles / "main.css").write_bytes(b"body{}")
    _point_dir(mocker, "styles_dir", styles)

    assert fs_in.get_style("main.css") == b"body{}"


def test_get_style_missing_returns_none(mocker: MockerFixture, tmp_path: Path) -> None:
    _point_dir(mocker, "styles_dir", tmp_path / "styles")

    assert fs_in.get_style("nope.css") is None


def test_get_style_blocks_path_traversal(mocker: MockerFixture, tmp_path: Path) -> None:
    styles = tmp_path / "styles"
    styles.mkdir()
    (tmp_path / "secret.txt").write_bytes(b"top secret")
    _point_dir(mocker, "styles_dir", styles)

    assert fs_in.get_style("../secret.txt") is None


def test_get_script_reads_existing_file(mocker: MockerFixture, tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "htmx.js").write_bytes(b"htmx")
    _point_dir(mocker, "scripts_dir", scripts)

    assert fs_in.get_script("htmx.js") == b"htmx"


def test_get_script_missing_returns_none(mocker: MockerFixture, tmp_path: Path) -> None:
    _point_dir(mocker, "scripts_dir", tmp_path / "scripts")

    assert fs_in.get_script("htmx.js") is None

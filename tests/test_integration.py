import os
import shutil
from pathlib import Path
from sphinx.application import Sphinx
from dotenv import load_dotenv
import pytest


@pytest.fixture(scope="function")
def run_sphinx(tmpdir, monkeypatch):
    """Fixture to run Sphinx builds using the real conf.py, repo_manifest.yml, and .env."""
    src = tmpdir.join("src")
    out = tmpdir.join("out")

    # Ensure src and out directories exist
    if not src.check():
        src.mkdir()
    if not out.check():
        out.mkdir()

    # Load environment variables from {root}/docs/.env
    project_root = Path(__file__).parent.parent
    load_dotenv(dotenv_path=project_root / "docs" / ".env")

    # Mock environment variables in the test environment
    for key, value in os.environ.items():
        monkeypatch.setenv(key, value)

    def run():
        Sphinx(
            srcdir=str(src),
            confdir=str(src),
            outdir=str(out),
            doctreedir=str(tmpdir.join("doctrees")),
            buildername="html",
        ).build()

    return run


def test_basic_build(run_sphinx, tmpdir):
    """Test that a basic build succeeds with the real conf.py."""
    src = tmpdir.join("src")
    if not src.check():
        src.mkdir()

    # Copy conf.py and repo_manifest.yml
    project_root = Path(__file__).parent.parent
    shutil.copy(project_root / "docs" / "source" / "conf.py", src.join("conf.py").strpath)
    shutil.copy(project_root / "docs" / "repo_manifest.yml", src.join("repo_manifest.yml").strpath)

    # Run Sphinx build
    run_sphinx()
    assert tmpdir.join("out", "index.html").check(), "HTML output not generated."


def test_extension_loaded(run_sphinx, tmpdir):
    """Test that the extension is loaded properly."""
    src = tmpdir.join("src")
    if not src.check():
        src.mkdir()

    # Write conf.py to src directory
    conf_py = """\
extensions = ['sphinx_repo_manager']
"""
    src.join("conf.py").write_text(conf_py, encoding="utf-8")

    # Write index.rst to src directory
    src.join("index.rst").write_text(
        """\
Hello Sphinx!
=============

This is a test page for the extension.
""",
        encoding="utf-8",
    )

    # Copy repo_manifest.yml
    project_root = Path(__file__).parent.parent
    shutil.copy(project_root / "docs" / "repo_manifest.yml", src.join("repo_manifest.yml").strpath)

    # Run Sphinx build
    run_sphinx()
    html = tmpdir.join("out", "index.html").read_text()
    assert "Hello Sphinx!" in html, "Expected content not found in the output HTML."

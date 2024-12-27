import os
from pathlib import Path
from sphinx.application import Sphinx
import pytest
import shutil

# Centralized paths for src->dest files
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONF_SRC = PROJECT_ROOT / "docs" / "source" / "conf.py"
MANIFEST_SRC = PROJECT_ROOT / "docs" / "repo_manifest.yml"
ENV_SRC = PROJECT_ROOT / "docs" / ".env"  # Add .env file path

# Directory structure relative to tmpdir
DOCS_RELATIVE = Path("docs")
SRC_RELATIVE = DOCS_RELATIVE / "source"
OUT_RELATIVE = Path("out")
DOCTREE_RELATIVE = Path("doctrees")


@pytest.mark.order(1)
def test_debug_paths():
    """Show these logs by appending `-s` arg to pytest."""
    print()
    print()
    print("-- PATHS ------------------------------------------------------------------------------------")
    print()
    print(f"- PROJECT_ROOT: '{PROJECT_ROOT}'")
    print(f"- CONF_SRC: '{CONF_SRC}'")
    print(f"- MANIFEST_SRC: '{MANIFEST_SRC}'")
    print(f"- ENV_SRC: '{ENV_SRC}'")
    print()
    print(f"- DOCS_RELATIVE: '{DOCS_RELATIVE}'")
    print(f"- SRC_RELATIVE: '{SRC_RELATIVE}'")
    print(f"- DOCTREE_RELATIVE: '{DOCTREE_RELATIVE}'")
    print()
    print(f"-- ENV VARIABLES --------------------------------------------------------------------------")
    print(f"- REPO_AUTH_USER (optional; falls back to 'oauth2'): '{os.getenv('REPO_AUTH_USER')}'")
    print(f"- REPO_AUTH_TOKEN (exists?): '{bool(os.getenv('REPO_AUTH_TOKEN'))}'")
    print(f"-- /PATHS -----------------------------------------------------------------------------------")
    print()


@pytest.fixture(scope="function")
def run_sphinx(tmpdir, monkeypatch):
    """
    Fixture to run Sphinx builds using the real conf.py, repo_manifest.yml, and .env.
    Returns:
        run: Callable to run the Sphinx build.
        docs: Path to the docs directory.
        src: Path to the Sphinx source directory.
        out: Path to the Sphinx output directory
    """
    # Centralized absolute paths for the test dirs
    docs = Path(tmpdir) / DOCS_RELATIVE
    src = Path(tmpdir) / SRC_RELATIVE
    out = Path(tmpdir) / OUT_RELATIVE
    doctree = Path(tmpdir) / DOCTREE_RELATIVE

    # Ensure dirs exist
    for path in [docs, src, out, doctree]:
        path.mkdir(parents=True, exist_ok=True)

    # Copy over the .env + repo_manifest.yml files
    shutil.copy(MANIFEST_SRC, docs / "repo_manifest.yml")
    shutil.copy(ENV_SRC, docs / ".env")  # Place .env file in docs

    def run():
        # Set the working dir to mimic the Sphinx source dir
        monkeypatch.chdir(src)

        # Run Sphinx
        Sphinx(
            srcdir=str(src),
            confdir=str(src),
            outdir=str(out),
            doctreedir=str(doctree),
            buildername="html",  # Similar to `make html`
        ).build()

    return run, docs, src, out


def test_basic_build(run_sphinx, tmpdir):
    """Test that a basic build succeeds with the real conf.py."""
    sphinx_runner, docs, src, out = run_sphinx

    shutil.copy(CONF_SRC, src / "conf.py")

    index_src = PROJECT_ROOT / "docs" / "source" / "index.rst"
    shutil.copy(index_src, src / "index.rst")

    sphinx_runner()
    assert (out / "index.html").exists(), "HTML output not generated."


def test_extension_loaded(run_sphinx, tmpdir):
    """Test that the extension is loaded properly."""
    run_sphinx, docs, src, out = run_sphinx

    # Write conf.py to src directory
    conf_py = """\
extensions = ['sphinx_repo_manager']
"""
    (src / "conf.py").write_text(conf_py, encoding="utf-8")

    # Write index.rst to src directory
    (src / "index.rst").write_text(
        """\
Hello Sphinx!
=============

Test extension page.
""",
        encoding="utf-8",
    )

    # Run Sphinx build
    run_sphinx()
    html = (out / "index.html").read_text()
    assert "Hello Sphinx!" in html, "Expected content not found in the output HTML."

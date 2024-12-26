import shutil
from pathlib import Path
import os
import pytest
from sphinx.application import Sphinx
import shutil
from pathlib import Path


@pytest.fixture(scope='function')
def run_sphinx(tmpdir):
    """Fixture to run Sphinx builds using the real conf.py and repo_manifest.yml."""
    src = tmpdir.mkdir('src')
    out = tmpdir.mkdir('out')

    # Path to the real conf.py and repo_manifest.yml
    project_root = Path(__file__).parent.parent  # Adjust based on your structure
    shutil.copy(project_root / "docs" / "source" / "conf.py", src.join('conf.py').strpath)

    # Copy repo_manifest.yml directly into the test directory
    shutil.copy(project_root / "docs" / "repo_manifest.yml", tmpdir.join('repo_manifest.yml').strpath)

    # Create a basic index.rst for the test
    src.join('index.rst').write_text("""
    Hello Sphinx!
    =============

    This is a test page.
    """, encoding='utf-8')

    def run():
        Sphinx(
            srcdir=src.strpath,
            confdir=src.strpath,
            outdir=out.strpath,
            doctreedir=out.join('.doctrees').strpath,
            buildername='html'
        ).build()

    return run


def test_basic_build(run_sphinx, tmpdir):
    """Test that a basic build succeeds with the real conf.py."""
    run_sphinx()
    assert tmpdir.join('out', 'index.html').check(), "HTML output was not generated."


def test_extension_loaded(run_sphinx, tmpdir):
    """Test that the extension is loaded properly."""
    src = tmpdir.mkdir('src') if not tmpdir.join('src').check() else tmpdir.join('src')

    conf_py = """
    extensions = ['sphinx_repo_manager']
    """
    src.join('conf.py').write_text(conf_py, encoding='utf-8')

    src.join('index.rst').write_text("""
    Hello Sphinx!
    =============

    This is a test page for the extension.
    """, encoding='utf-8')

    run_sphinx()
    html = tmpdir.join('out', 'index.html').read()
    assert "Hello Sphinx!" in html, "Expected content not found in the output HTML."

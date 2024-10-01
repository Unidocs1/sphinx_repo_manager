# source/_extensions/sphinx_openapi/__init__.py
from .sphinx_openapi import SphinxOpenApi
from sphinx.application import Sphinx


# ENTRY POINT >>
def setup(app: Sphinx):
    app.add_config_value("openapi_spec_url_noext", "", "env", [str])
    app.add_config_value("openapi_dir_path", "_specs", "env", [str])
    app.add_config_value("openapi_generated_file_posix_path", "", "env", [str])
    app.add_config_value("openapi_file_type", "json", "env", [str])

    openapi_downloader = SphinxOpenApi(app)
    app.connect("builder-inited", openapi_downloader.setup_openapi)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

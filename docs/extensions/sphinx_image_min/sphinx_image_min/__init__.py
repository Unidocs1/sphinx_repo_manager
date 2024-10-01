# source/_extensions/sphinx_image_min/__init__.py
from sphinx.application import Sphinx
from .sphinx_image_min import SphinxImageMin, optimize_images


# ENTRY POINT >>
def setup(app: Sphinx):
    # Configuration values for the extension
    app.add_config_value("img_optimization_enabled", True, "env", [bool])
    app.add_config_value("img_optimization_max_width", 1920, "env", [int])

    # Register the directive, even if it doesn't do anything specific right now
    app.add_directive("optimize-images", SphinxImageMin)

    # Connect the optimization function to the build-finished event
    app.connect("build-finished", optimize_images)

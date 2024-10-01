# source/_extensions/sphinx_feature_flags/__init__.py
from sphinx.application import Sphinx
from .sphinx_feature_flags import (
    SphinxFeatureFlags,
    feature_flag_node,
    visit_feature_flag_node,
    depart_feature_flag_node,
)


# ENTRY POINT >>
def setup(app: Sphinx):
    app.add_config_value("feature_flags", {}, "env", [dict])
    app.add_directive("feature-flag", SphinxFeatureFlags)
    app.add_node(
        feature_flag_node, html=(visit_feature_flag_node, depart_feature_flag_node)
    )

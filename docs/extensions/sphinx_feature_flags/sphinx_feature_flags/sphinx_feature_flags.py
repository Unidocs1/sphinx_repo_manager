"""
Xsolla Sphinx Extension: sphinx_feature_flags
- See README for more info
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util.docutils import SphinxDirective


class feature_flag_node(nodes.General, nodes.Element):
    pass


class SphinxFeatureFlags(SphinxDirective):
    has_content = True
    required_arguments = 1
    option_spec = {
        "fallback": directives.flag,
    }

    def run(self):
        flag_name = self.arguments[0]
        is_fallback = "fallback" in self.options

        feature_flag_enabled = self.env.config.feature_flags.get(flag_name, False)

        if feature_flag_enabled and not is_fallback:
            node = feature_flag_node()
            self.state.nested_parse(self.content, self.content_offset, node)
            return [node]
        elif not feature_flag_enabled and is_fallback:
            node = feature_flag_node()
            self.state.nested_parse(self.content, self.content_offset, node)
            return [node]
        else:
            return []


def visit_feature_flag_node(self, node):
    pass


def depart_feature_flag_node(self, node):
    pass

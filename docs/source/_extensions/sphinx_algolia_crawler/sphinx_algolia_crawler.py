"""
Xsolla Sphinx Extension: sphinx_algolia_crawler
- See README for more info
"""
import os
import subprocess
from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class algolia_crawler_node(nodes.General, nodes.Element):
    """ Custom node for capturing the output of the Algolia crawler execution. """
    pass


class SphinxAlgoliaCrawler(SphinxDirective):
    """
    Sphinx directive to execute the Algolia DocSearch scraper during the Sphinx build process.
    - Checks for the presence of `.env` and `config.json`.
    - Runs the DocSearch scraper using Docker if the necessary files are present.
    """
    has_content = True
    required_arguments = 0
    option_spec = {
        'config': str,
    }

    def run(self):
        config_file = self.options.get('config', 'config.json')
        config_path = os.path.abspath(config_file)

        if not os.path.exists(config_path):
            error = self.state_machine.reporter.error(
                f"[sphinx_algolia_crawler] Config file '{config_path}' not found.",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        env_file = os.path.join(os.path.dirname(__file__), '.env')
        if not os.path.exists(env_file):
            warning = self.state_machine.reporter.warning(
                f"[sphinx_algolia_crawler] .env file not found at '{env_file}'. See .env.template for guidance.",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [warning]

        try:
            result = run_docker_scraper(env_file, config_path)

            success_message = f"[sphinx_algolia_crawler] DocSearch scraper completed successfully:\n{result.stdout}"
            node = algolia_crawler_node()
            node += nodes.paragraph(text=success_message)

            return [node]
        except subprocess.CalledProcessError as e:
            error_message = f"[sphinx_algolia_crawler] Error running DocSearch scraper:\n{e.stderr}"
            error = self.state_machine.reporter.error(
                error_message,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]


def run_docker_scraper(env_file, config_path):
    """
    Runs the Docker-based DocSearch scraper.
    - Uses the specified `.env` and `config.json` files.
    """
    args = [
        'docker', 'run', '-it',
        '--env-file', env_file,
        '-e', f"CONFIG=$(cat {config_path} | jq -r tostring)",
        'algolia/docsearch-scraper'
    ]

    return subprocess.run(
        args,
        check=True,
        capture_output=True,
        shell=True,
        text=True,
    )


# ENTRY POINT (Sphinx) >>
def setup(app):
    """
    Entry point for the Sphinx extension.
    """
    app.add_directive('algolia-crawler', SphinxAlgoliaCrawler)


# ENTRY POINT (Standalone) >>
is_standalone = __name__ == "__main__"
if is_standalone:
    """
    Standalone execution of the script.
    - Checks for `.env` in the current directory.
    - Executes the Docker-based DocSearch scraper if `.env` is found.
    """
    env_file_path = './.env'
    if os.path.exists(env_file_path):
        try:
            run_docker_scraper(env_file_path, './config.json')
        except subprocess.CalledProcessError as e:
            print(f"Error running DocSearch scraper: {e.stderr}")
    else:
        print(f".env file not found at '{env_file_path}': See '.env.template.'")

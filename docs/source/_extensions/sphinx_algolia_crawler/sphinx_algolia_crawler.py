"""
Xsolla Sphinx Extension: sphinx_algolia_crawler
- See README for more info
"""
from docutils import nodes
from sphinx.util.docutils import SphinxDirective
import os
import subprocess
import json


class algolia_crawler_node(nodes.General, nodes.Element):
    """ Custom node for capturing the output of the Algolia crawler execution. """
    pass


class SphinxAlgoliaCrawler(SphinxDirective):
    """
    Sphinx directive to execute the Algolia DocSearch scraper during the Sphinx build process.
    - Checks for the presence of `.env` and the appropriate config file based on the stage.
    - Runs the DocSearch scraper using Docker if the necessary files are present.
    """
    has_content = True
    required_arguments = 0
    option_spec = {
        'config': str,
    }

    def run(self):
        # Determine the configuration stage (e.g., dev_stage, production_stage, or none)
        stage = self.env.config.algolia_crawler_config_stage

        # Exit if the stage is set to 'none'
        if stage == 'none':
            return []

        config_filename = 'config.dev.json' if stage == 'dev_stage' else 'config.prod.json'
        print(f"[sphinx_algolia_crawler] Config file: {config_filename}")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, self.options.get('config', config_filename))

        if not os.path.exists(config_file_path):
            error = self.state_machine.reporter.error(
                f"Config file '{config_file_path}' not found.",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        env_file = os.path.join(script_dir, '.env')
        if not os.path.exists(env_file):
            warning = self.state_machine.reporter.warning(
                f".env file not found at '{env_file}'. See .env.template for guidance.",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [warning]

        try:
            result = run_docker_scraper(env_file, config_file_path)

            success_message = f"DocSearch scraper completed successfully:\n{result.stdout}"
            node = algolia_crawler_node()
            node += nodes.paragraph(text=success_message)

            return [node]
        except subprocess.CalledProcessError as e:
            error_message = f"Error running DocSearch scraper:\n{e.stderr}"
            error = self.state_machine.reporter.error(
                error_message,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]


def run_docker_scraper(env_file, json_config_path):
    """
    Runs the Docker-based DocSearch scraper.
    - Emulates the behavior of 'CONFIG=$(cat config.json | jq -r tostring)'
    """
    # Read and load the JSON file content
    with open(json_config_path, 'r') as file:
        config_content = json.load(file)

    # Convert the JSON object to a compact, single-line string
    compact_json_string = json.dumps(config_content)

    # Construct the Docker command
    args = [
        'docker', 'run', '-it',
        '--env-file', env_file,
        '-e', f'CONFIG={compact_json_string}',
        'algolia/docsearch-scraper'
    ]

    # Print the full Docker command for debugging
    # print(f"[sphinx_algolia_crawler] Running Docker command: {' '.join(args)}")

    # Run the Docker command
    return subprocess.run(
        args,
        check=True,
        capture_output=False,  # Set to True if you want to capture the output
        shell=False,
        text=True,
    )


# ENTRY POINT (Sphinx) >>
def setup(app):
    """
    Entry point for the Sphinx extension.
    """
    # Add the configuration stage setting to Sphinx
    app.add_config_value('algolia_crawler_config_stage', 'dev_stage', 'env')

    # Only add the directive if the extension is not set to 'none'
    if app.config.algolia_crawler_config_stage != 'none':
        app.add_directive('algolia-crawler', SphinxAlgoliaCrawler)


# ENTRY POINT (Standalone) >>
is_standalone = __name__ == "__main__"
if is_standalone:
    """
    Standalone execution of the script.
    - Checks for `.env` in the current directory.
    - Executes the Docker-based DocSearch scraper if `.env` is found.
    """
    script_dir = os.path.normpath(os.path.abspath(
        os.path.dirname(os.path.abspath(__file__))))
    stage = 'dev_stage'  # Default to dev_stage in standalone mode
    config_filename = 'config.dev.json' if stage == 'dev_stage' else 'config.prod.json'
    env_file_path = os.path.join(script_dir, '.env')
    config_file_path = os.path.join(script_dir, config_filename)

    if stage == 'none':
        print("[sphinx_algolia_crawler] stage is 'none'; skipping this extension!")
        exit(0)

    if not os.path.exists(env_file_path):
        raise FileNotFoundError(f".env file not found at '{env_file_path}': See '.env.template.'")
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Json Config file '{config_file_path}' not found.")

    if os.path.exists(env_file_path):
        try:
            run_docker_scraper(env_file_path, config_file_path)
        except subprocess.CalledProcessError as e:
            print(f"[sphinx_algolia_crawler] Error running DocSearch scraper: {e.stderr}")
    else:
        print(f"[sphinx_algolia_crawler] .env file not found at '{env_file_path}': See '.env.template.'")

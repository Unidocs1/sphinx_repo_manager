"""
Xsolla Sphinx Extension: sphinx_algolia_crawler
- See README for more info
"""
import os
import sys
import subprocess
import json


class SphinxAlgoliaCrawler:
    """
    A class to execute the Algolia DocSearch scraper during the Sphinx build process.
    - Checks for the presence of `.env` and the appropriate config file based on the stage.
    - Runs the DocSearch scraper using Docker if the necessary files are present.
    """

    def run(self, stage, script_dir):
        """
        Run the Algolia DocSearch scraper based on the provided stage.
        """
        if stage == 'none':
            return

        config_filename = 'config.dev.json' if stage == 'dev_stage' else 'config.prod.json'
        print(f"\n[sphinx_algolia_crawler] Config file: {config_filename}")

        config_file_path = os.path.join(script_dir, config_filename)

        if not os.path.exists(config_file_path):
            print(f"[sphinx_algolia_crawler] Config file '{config_file_path}' not found.")
            return

        env_file = os.path.join(script_dir, '.env')
        if not os.path.exists(env_file):
            print(f"[sphinx_algolia_crawler] .env file not found at '{env_file}'. See .env.template for guidance.")
            return

        try:
            result = self.run_docker_scraper(env_file, config_file_path)
            print(f"[sphinx_algolia_crawler] DocSearch scraper completed successfully:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"[sphinx_algolia_crawler] Error running DocSearch scraper:\n{e.stderr}")

    @staticmethod
    def run_docker_scraper(env_file, json_config_path):
        """
        Runs the Docker-based DocSearch scraper.
        - Emulates the behavior of 'CONFIG=$(cat config.json | jq -r tostring)'
        """
        with open(json_config_path, 'r') as file:
            config_content = json.load(file)

        compact_json_string = json.dumps(config_content)

        args = [
            'docker', 'run', '-it',
            '--env-file', env_file,
            '-e', f'CONFIG={compact_json_string}',
            'algolia/docsearch-scraper'
        ]

        print(f"Running Docker command: {' '.join(args)}")

        return subprocess.run(
            args,
            check=True,
            capture_output=False,
            shell=False,
            text=True,
        )


# ENTRY POINT (Sphinx) >>
def setup(app):
    """
    Entry point for the Sphinx extension.
    """
    app.add_config_value('algolia_crawler_config_stage', 'dev_stage', 'env')

    def on_build_finished(app, exception):
        stage = app.config.algolia_crawler_config_stage
        script_dir = os.path.abspath(os.path.dirname(__file__))
        if stage:
            crawler = SphinxAlgoliaCrawler()
            crawler.run(stage, script_dir)

    app.connect('build-finished', on_build_finished)


# ENTRY POINT (Standalone) >>
if __name__ == "__main__":
    """
    Standalone execution of the script.
    - Requires the config file name to be passed as the first argument.
    - Checks for `.env` in the current directory.
    - Executes the Docker-based DocSearch scraper if `.env` is found.
    """
    if len(sys.argv) < 2:
        print("[sphinx_algolia_crawler] Error: You must provide the config file name as the first argument.")
        sys.exit(1)

    config_filename = sys.argv[1]  # eg: 'config.dev.json'
    script_dir = os.path.normpath(os.path.abspath(
        os.path.dirname(os.path.abspath(__file__))))
    env_file_path = os.path.join(script_dir, '.env')
    config_file_path = os.path.join(script_dir, config_filename)

    if not os.path.exists(env_file_path):
        raise FileNotFoundError(
            f"[sphinx_algolia_crawler] .env file not found at '{env_file_path}': See '.env.template.'")
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"[sphinx_algolia_crawler] Json Config file '{config_file_path}' not found.")

    try:
        crawler = SphinxAlgoliaCrawler()
        crawler.run('custom', script_dir)
    except subprocess.CalledProcessError as e:
        print(f"[sphinx_algolia_crawler] Error running DocSearch scraper: {e.stderr}")

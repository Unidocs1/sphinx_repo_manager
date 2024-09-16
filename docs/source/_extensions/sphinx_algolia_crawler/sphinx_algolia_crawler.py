"""
Xsolla Sphinx Extension: sphinx_algolia_crawler
- See README for more info
"""
import base64
import os
import requests
import argparse
from dotenv import load_dotenv  # Import the dotenv package to load .env

# Load environment variables from the .env file (for local testing)
load_dotenv()


class SphinxAlgoliaCrawler:
    """
    A class to trigger the Algolia DocSearch crawler during the Sphinx build process.
    - Uses the Algolia API to reindex the crawler.
    """

    def __init__(self, algolia_crawler_user_id, algolia_crawler_api_key, algolia_crawler_id, script_dir):
        self.algolia_crawler_user_id = algolia_crawler_user_id
        self.algolia_crawler_api_key = algolia_crawler_api_key
        self.algolia_crawler_id = algolia_crawler_id
        self.script_dir = script_dir

    def run(self):
        """
        Trigger the Algolia DocSearch crawler via the Algolia API.
        """
        print(f"\n[sphinx_algolia_crawler] Determining if we should run Algolia DocSearch crawler...")

        if not self.algolia_crawler_user_id:
            print("[sphinx_algolia_crawler] .env `ALGOLIA_CRAWLER_USER_ID` missing; skipping crawler trigger.\n")
            return

        if not self.algolia_crawler_api_key:
            print("[sphinx_algolia_crawler] .env `ALGOLIA_CRAWLER_API_KEY` missing; skipping crawler trigger.\n")
            return

        if not self.algolia_crawler_id:
            print(f"[sphinx_algolia_crawler] No `ALGOLIA_CRAWLER_ID` provided; skipping crawler trigger.\n")
            return

        result = None  # Initialize result to None to avoid referencing before assignment
        try:
            result = self.trigger_algolia_crawler()
            result.raise_for_status()  # Raise an exception for HTTP error responses
            crawler_id_last_4 = self.algolia_crawler_id[-4:]
            print(f"[sphinx_algolia_crawler] Crawler triggered successfully for crawler_id '...{crawler_id_last_4}'\n")
        except requests.HTTPError as http_err:
            if result is not None:
                try:
                    error_info = result.json().get('error', {})
                    error_code = error_info.get('code', 'N/A')
                    error_message = error_info.get('message', 'No error message provided')
                    print(f"[sphinx_algolia_crawler] HTTP error occurred: "
                          f"{http_err.response.status_code} - {error_code} - {error_message}\n")
                except ValueError:
                    # Handle case where response body isn't JSON
                    print(f"[sphinx_algolia_crawler] HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}\n")
            else:
                print(f"[sphinx_algolia_crawler] HTTP error occurred but no response to parse: {http_err}\n")
        except requests.RequestException as e:
            print(f"[sphinx_algolia_crawler] Error triggering Algolia crawler: {str(e)}\n")

    def trigger_algolia_crawler(self):
        """
        Triggers the Algolia crawler via their API using Basic Authentication.
        """
        url = f"https://crawler.algolia.com/api/1/crawlers/{self.algolia_crawler_id}/reindex"
        credentials = f"{self.algolia_crawler_user_id}:{self.algolia_crawler_api_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode("utf-8")

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        return requests.post(url, headers=headers)


# ENTRY POINT (Sphinx) >>
def setup(app):
    """
    Entry point for the Sphinx extension.
    """
    app.add_config_value('algolia_crawler_enabled', False, rebuild=False)

    def on_build_finished(app, exception):
        if not app.config.algolia_crawler_enabled:
            print(f"\n[sphinx_algolia_crawler] Crawler not enabled in this env; skipping extension.\n")
            return

        algolia_crawler_user_id = os.getenv('ALGOLIA_CRAWLER_USER_ID')
        algolia_crawler_api_key = os.getenv('ALGOLIA_CRAWLER_API_KEY')
        algolia_crawler_id = os.getenv('ALGOLIA_CRAWLER_ID')
        script_dir = os.path.abspath(os.path.dirname(__file__))

        crawler = SphinxAlgoliaCrawler(
            algolia_crawler_user_id,
            algolia_crawler_api_key,
            algolia_crawler_id,
            script_dir
        )
        crawler.run()

    app.connect('build-finished', on_build_finished, priority=800)


# ENTRY POINT (Standalone) >>
if __name__ == "__main__":
    """
    Standalone execution of the script.
    - Requires the Crawler User ID and API Key as arguments.
    """
    parser = argparse.ArgumentParser(description="Trigger the Algolia DocSearch Crawler | "
                                                 "https://www.algolia.com/doc/rest-api/crawler/")
    parser.add_argument('--crawler_user_id', required=True)
    parser.add_argument('--crawler_api_key', required=True)
    parser.add_argument('--crawler_id', required=True)
    args = parser.parse_args()

    script_dir = os.path.normpath(os.path.abspath(
        os.path.dirname(os.path.abspath(__file__))))

    try:
        crawler = SphinxAlgoliaCrawler(
            args.crawler_user_id,
            args.crawler_api_key,
            args.crawler_id,
            script_dir,
        )
        crawler.run()
    except requests.RequestException as e:
        print(f"[sphinx_algolia_crawler-standalone] Error triggering Algolia crawler: {str(e)}")

"""
Xsolla Sphinx Extension: sphinx_algolia_crawler
- See README for more info
"""
import os
import requests
import argparse


class SphinxAlgoliaCrawler:
    """
    A class to trigger the Algolia DocSearch crawler during the Sphinx build process.
    - Uses the Algolia API to reindex the crawler.
    """

    def __init__(
            self,
            app_id,
            secret_write_api_key,
            crawler_id,
            script_dir
    ):
        self.app_id = app_id
        self.secret_write_api_key = secret_write_api_key
        self.script_dir = script_dir
        self.crawler_id = crawler_id

    def run(self):
        """
        Trigger the Algolia DocSearch crawler via the Algolia API.
        """
        if not self.app_id or not self.secret_write_api_key:
            print("[sphinx_algolia_crawler] App ID or API key not provided, skipping crawler trigger.")
            return

        if not self.crawler_id:
            print(f"[sphinx_algolia_crawler] No crawler ID provided, skipping crawler trigger.")
            return

        try:
            result = self.trigger_algolia_crawler(self.crawler_id)
            if result.status_code == 200:
                print("[sphinx_algolia_crawler] Crawler triggered successfully.")
            else:
                print(f"[sphinx_algolia_crawler] Failed to trigger crawler: "
                      f"Error {result.status_code} - {result.text}")
        except requests.RequestException as e:
            print(f"[sphinx_algolia_crawler] Error triggering Algolia crawler: {str(e)}")

    def trigger_algolia_crawler(self, crawler_id):
        """
        Triggers the Algolia crawler via their API.
        """
        url = f"https://crawler.algolia.com/api/1/crawlers/{crawler_id}/reindex"
        headers = {
            "X-Algolia-API-Key": self.secret_write_api_key,
            "X-Algolia-Application-Id": self.app_id,
        }

        return requests.post(url, headers=headers)


# ENTRY POINT (Sphinx) >>
def setup(app):
    """
    Entry point for the Sphinx extension.
    """
    app.add_config_value('algolia_crawler_enabled', False, 'env')
    app.add_config_value('algolia_crawler_app_id', '', 'env')
    app.add_config_value('algolia_crawler_secret_api_key', '', 'env')
    app.add_config_value('algolia_crawler_id', '', 'env')

    def on_build_finished(app, exception):
        if app.config.algolia_crawler_enabled:
            app_id = app.config.algolia_crawler_app_id
            secret_write_api_key = app.config.algolia_crawler_secret_write_api_key
            crawler_id = app.config.algolia_crawler_id
            script_dir = os.path.abspath(os.path.dirname(__file__))

            crawler = SphinxAlgoliaCrawler(
                app_id,
                secret_write_api_key,
                crawler_id,
                script_dir)
            crawler.run()

    app.connect('build-finished', on_build_finished)


# ENTRY POINT (Standalone) >>
if __name__ == "__main__":
    """
    Standalone execution of the script.
    - Requires the App ID and API Key as arguments.
    """
    parser = argparse.ArgumentParser(description="Trigger the v1 Algolia DocSearch Crawler | "
                                                 "https://www.algolia.com/doc/rest-api/crawler/")
    parser.add_argument('--app_id', required=True, help="The public Algolia App id")
    parser.add_argument('--api_key', required=True, help="The secret Algolia API write key")
    parser.add_argument('--crawler_id', required=True, help="The crawler id (not index name)")
    args = parser.parse_args()

    script_dir = os.path.normpath(os.path.abspath(
        os.path.dirname(os.path.abspath(__file__))))

    try:
        crawler = SphinxAlgoliaCrawler(
            args.app_id,
            args.api_key,
            args.crawler_id,
            script_dir)
        crawler.run()
    except requests.RequestException as e:
        print(f"[sphinx_algolia_crawler] Error triggering Algolia crawler: {str(e)}")

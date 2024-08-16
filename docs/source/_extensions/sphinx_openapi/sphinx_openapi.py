"""
Xsolla Sphinx Extension: sphinx_openapi
- See README for more info
"""
import os
import requests
from pathlib import Path
from enum import Enum
from requests.exceptions import Timeout
from sphinx.application import Sphinx


class OpenApiFileType(Enum):
    JSON = 'json'
    YAML = 'yaml'


class SphinxOpenApi:
    def __init__(self, app: Sphinx):
        self.app = app
        self.openapi_spec_url_noext = app.config.openapi_spec_url_noext
        self.openapi_dir_path = app.config.openapi_dir_path
        self.openapi_generated_file_posix_path = app.config.openapi_generated_file_posix_path
        self.openapi_file_type = OpenApiFileType[app.config.openapi_file_type.upper()]
        self.openapi_file_path_no_ext = os.path.normpath(
            os.path.join(self.openapi_dir_path, f'openapi'))
        self.openapi_file_path = os.path.normpath(
            os.path.join(self.openapi_dir_path, f'openapi.{self.openapi_file_type.value}'))

    @staticmethod
    def download_file(url, save_to_path, timeout=5):
        try:
            # Attempt to get the response with the specified timeout
            response = requests.get(url, timeout=timeout)
    
            # Check if the response was successful; if not, raise an HTTPError
            response.raise_for_status()
    
            # If successful, write the content to the file
            with open(save_to_path, 'wb') as f:
                f.write(response.content)
            print(f"[sphinx_openapi.py] Successfully downloaded {url} to: '{save_to_path}'")
    
        except Timeout:
            print(f'[sphinx_openapi.py] Timeout occurred while downloading: {url}')
    
        except requests.exceptions.HTTPError as http_err:
            # Capture HTTP errors and print the status code and response content
            print(f'[sphinx_openapi.py] HTTP error occurred while downloading: {url}: {http_err}')
            print(f'[sphinx_openapi.py] HTTP response content: {http_err.response.text}')
    
        except requests.exceptions.SSLError as ssl_err:
            # Capture SSL errors and print the specific SSL error
            print(f'[sphinx_openapi.py] SSL error occurred while downloading {url}: {ssl_err}')
    
        except requests.exceptions.RequestException as req_err:
            # Capture any other request-related exceptions and print the error
            print(f'[sphinx_openapi.py] Failed to download {url}: {req_err}')
    
        except Exception as e:
            # Capture any unexpected exceptions
            print(f'[sphinx_openapi.py] An unexpected error occurred while downloading {url}: {e}')

    def setup_openapi(self, app):
        print('')
        print('[sphinx_openapi.py] Attempting to download schema files...')

        if not os.path.exists(self.openapi_dir_path):
            os.makedirs(self.openapi_dir_path)

        try:
            self.download_file(f'{self.openapi_spec_url_noext}.json', self.openapi_file_path_no_ext + '.json')
        except Exception as e:
            print(f'[sphinx_openapi.py] Failed to download {self.openapi_spec_url_noext}.json: {e}')
            return

        try:
            self.download_file(f'{self.openapi_spec_url_noext}.yaml', self.openapi_file_path_no_ext + '.yaml')
        except Exception as e:
            print(f'[sphinx_openapi.py] Failed to download {self.openapi_spec_url_noext}.yaml: {e}')
            return

        print(f"[sphinx_openapi.py] OpenAPI spec file available at '{self.openapi_generated_file_posix_path}'")


# ENTRY POINT >>
def setup(app: Sphinx):
    app.add_config_value('openapi_spec_url_noext', '', 'env')
    app.add_config_value('openapi_dir_path', '_specs', 'env')
    app.add_config_value('openapi_generated_file_posix_path', '', 'env')
    app.add_config_value('openapi_file_type', 'json', 'env')

    openapi_downloader = SphinxOpenApi(app)
    app.connect('builder-inited', openapi_downloader.setup_openapi)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

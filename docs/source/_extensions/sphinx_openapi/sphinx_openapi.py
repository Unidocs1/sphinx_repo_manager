"""
Xsolla Sphinx Extension: sphinx_openapi
- See README for more info
"""
import orjson  # Way more efficient than `json` lib for handling giant files
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

        # This is the file type we'll use for openapi docgen | json or yaml 
        self.openapi_file_type = OpenApiFileType[app.config.openapi_file_type.upper()]
        self.openapi_file_path_no_ext = os.path.normpath(
            os.path.join(self.openapi_dir_path, 'openapi'))
        self.openapi_file_path = f'{self.openapi_file_path_no_ext}.{self.openapi_file_type.value}'  # .json or .yaml

    def download_schema_files(self):
        try:
            self.download_file(self.openapi_spec_url_noext + '.json',
                               self.openapi_file_path_no_ext + '.json')
        except Exception as e:
            print(f'[sphinx_openapi.py] Failed to download "{self.openapi_spec_url_noext}.json": {e}')
            return

        try:
            self.download_file(self.openapi_spec_url_noext + '.yaml',
                               self.openapi_file_path_no_ext + '.yaml')
        except Exception as e:
            print(f'[sphinx_openapi.py] Failed to download "{self.openapi_spec_url_noext}.yaml": {e}')
            return

    def setup_openapi(self, app):
        print('')
        print('[sphinx_openapi.py] Attempting to download schema files...')

        if not os.path.exists(self.openapi_dir_path):
            os.makedirs(self.openapi_dir_path)

        self.download_schema_files()

        if self.openapi_file_type == OpenApiFileType.JSON:
            self.preprocess_json_schema_file()
        else:
            print(f"[sphinx_openapi] openapi_file_type ({self.openapi_file_type}) "
                  f"!= 'json'; skipping preprocessing...")

        print(f"[sphinx_openapi.py] Done:\n"
              f"- Generated from: {self.openapi_file_path}'"
              f"- Built to: 'build/html/{self.openapi_generated_file_posix_path}.html'\n")

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
            print(f"- Successfully downloaded {url} to: '{save_to_path}'")

        except Timeout:
            print(f'- Timeout occurred while downloading: {url}')
        except requests.exceptions.HTTPError as http_err:
            # Capture HTTP errors and print the status code and response content
            print(f'- HTTP error occurred while downloading: {url}: {http_err}')
            print(f'- HTTP response content: {http_err.response.text}')
        except requests.exceptions.SSLError as ssl_err:
            # Capture SSL errors and print the specific SSL error
            print(f'- SSL error occurred while downloading {url}: {ssl_err}')
        except requests.exceptions.RequestException as req_err:
            # Capture any other request-related exceptions and print the error
            print(f'- Failed to download {url}: {req_err}')
        except Exception as e:
            # Capture any unexpected exceptions
            print(f'- An unexpected error occurred while downloading {url}: {e}')

    # TODO: Add support for yaml
    def preprocess_json_schema_file(self):
        """ Reads json file, implement bug workarounds, adds logo """
        print('[sphinx_openapi.py] Preprocessing openapi.json (bug workarounds, inject logo)...')
        
        try:
            schema_file_name = self.openapi_file_path_no_ext + f'.{self.openapi_file_type.value}'
            schema_file_path = Path(self.openapi_dir_path, schema_file_name)

            # 1. Bug workarounds - Replace these refs with null:
            #   a. Invalid reference token: models.Address
            #   b. Invalid reference token: models.Defaults
            # 2. Injections:
            #   a. Add logo: `../../../_static/images/xbe_static_docs/logo.png`
            with open(schema_file_path, 'rb') as f:  # Reading in binary mode for orjson
                schema = orjson.loads(f.read())

            # (1) Bug fixes
            schema['components']['schemas']['models.Contact']['properties']['address']['$ref'] = None
            schema['components']['schemas']['models.Resource']['properties']['defaults']['$ref'] = None
            
            # (2) Injections
            schema['info']['x-logo'] = '../../../_static/images/xbe_static_docs/logo.png'

            # Save the schema back to the file, keeping it minimized
            with open(schema_file_path, 'wb') as f:  # Writing in binary mode for orjson
                f.write(orjson.dumps(schema))

        except Exception as e:
            raise Exception(f'[sphinx_openapi.py] Failed to preprocess_json_schema_file: {e}')


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

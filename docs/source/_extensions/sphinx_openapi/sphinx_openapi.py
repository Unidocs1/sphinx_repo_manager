"""
Xsolla Sphinx Extension: sphinx_openapi
- See README for more info
"""
import os
import requests
from pathlib import Path
from enum import Enum
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
    def download_file(url, save_to_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_to_path, 'wb') as f:
                f.write(response.content)
            print(f"[sphinx_openapi.py] Successfully downloaded {url} to: '{save_to_path}'")
        else:
            print(f'[sphinx_openapi.py] Failed to download {url}: {response.status_code}')

    def setup_openapi(self, app):
        print('')
        print('[sphinx_openapi.py] Starting...')

        if not os.path.exists(self.openapi_dir_path):
            os.makedirs(self.openapi_dir_path)

        try:
            self.download_file(f'{self.openapi_spec_url_noext}.json', self.openapi_file_path_no_ext + '.json')
        except Exception as e:
            print(f'[sphinx_openapi.py] Failed to download {self.openapi_spec_url_noext}.json: {e}')
        
        try:
            self.download_file(f'{self.openapi_spec_url_noext}.yaml', self.openapi_file_path_no_ext + '.yaml')
        except Exception as e:
            print(f'[sphinx_openapi.py] Failed to download {self.openapi_spec_url_noext}.yaml: {e}')

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

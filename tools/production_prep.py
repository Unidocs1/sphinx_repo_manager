""" Preps the project for production_stage. """
import argparse
import os
import yaml
import logging
import re
from colorama import init, Fore

# -- CUSTOMIZE ENV --------------------------------------------------------------------------------------------

target_new_ver = 'v2024.07.0'

# -- CLASS & LOG PREP ----------------------------------------------------------------------------------------- 

# Configure logging
class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.levelname = ''
        if record.levelno == logging.WARNING:
            record.levelname = ''
        if record.levelno == logging.ERROR:
            record.levelname = ''
        return super().format(record)


# Configure logging
formatter = CustomFormatter('%(levelname)s%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[handler])

# Define colors
ERR_COLOR = Fore.RED
SUCCESS_COLOR = Fore.GREEN
WARN_COLOR = Fore.YELLOW
FYI_COLOR = Fore.CYAN


class ProductionPrep:
    def __init__(self):
        init(autoreset=True)  # Initialize colorama
        self.launch_path = os.getcwd()
        self.test_index = 0

        self.repo_manifest_path = os.path.abspath(os.path.join(self.launch_path, '../docs/repo_manifest.yml'))
        self.repo_manifest_dir_path = os.path.dirname(self.repo_manifest_path)
        self.conf_dot_py_path = os.path.join(self.repo_manifest_dir_path, 'source/conf.py')

        self.manifest = self.load_manifest()
        self.manifest_repos = self.manifest['repositories']
        self.manifest_stage = self.manifest['stage']
        self.manifest_default_branch = self.manifest['default_branch']
        self.manifest_is_dev_stage = self.manifest_stage == 'dev_stage'
        self.xbe_static_docs_repo = self.manifest_repos['xbe_static_docs']
        self.manifest_target_prod_ver = self.xbe_static_docs_repo['production_stage']['checkout']

    # -- HELPERS --------------------------------------------------------------------------------------------- 

    @staticmethod
    def get_success_str():
        return "✅"

    @staticmethod
    def get_info_str():
        return "ℹ️"

    @staticmethod
    def get_fail_str():
        return "🔥"

    @staticmethod
    def get_warn_str():
        return "⚠️"

    def get_fallback_stage_info(self):
        fallback_stage_info = {
            'checkout': self.manifest_default_branch,
            'checkout_type': 'branch',
        }
        return fallback_stage_info

    def log_test_name(self, test_name):
        print(f'\n{self.get_test_index_str()} {test_name}():')

    def log_info(self, msg):
        print(f"  - {FYI_COLOR}{self.get_info_str()} {msg}{Fore.RESET}")

    def log_success(self, msg):
        print(f"  - {SUCCESS_COLOR}{self.get_success_str()} {msg}{Fore.RESET}")

    def log_warn(self, msg):
        print(f"  - {WARN_COLOR}{self.get_warn_str()} {msg}{Fore.RESET}")

    def log_fail(self, err_msg):
        if err_msg and isinstance(err_msg, str):
            err_msg = err_msg.replace("\\\\", "\\")  # path/to/ instead of path//to//
        logging.error(f"  - {ERR_COLOR}{self.get_fail_str()} {err_msg}{Fore.RESET}")

    def assert_complete(self):
        self.test_index += 1

    def get_test_index_str(self):
        return f"[{self.test_index}]"

    def load_manifest(self):
        """ Load the YAML manifest file and save it to self. """
        with open(self.repo_manifest_path, 'r') as file:
            return yaml.safe_load(file)

    # -- TESTS --------------------------------------------------------------------------------------------- 

    def assert_conf_dot_py(self):
        self.log_test_name('assert_conf_dot_py')

        try:
            # Read the conf.py file content
            with open(self.conf_dot_py_path, 'r') as conf_file:
                conf_content = conf_file.read()

            # Use a regular expression to find the `release` variable
            match = re.search(r"^release\s*=\s*['\"]([^'\"]+)['\"]", conf_content, re.MULTILINE)
            if match:
                release = match.group(1)
                expected = f"conf.py 'release' == '{target_new_ver}' (from manifest xbe_static_docs prod ver)"
                assert release == target_new_ver, f"Expected {expected} [got '{release}']"
                self.log_success(expected)
            else:
                raise AssertionError("Release variable not found in conf.py")

        except AssertionError as e:
            self.log_fail(e)
        except Exception as e:
            self.log_fail(f"Failed to analyze conf.py: {e}")
        self.assert_complete()

    def assert_manifest_repo_versions(self):
        self.log_test_name('assert_manifest_repo_versions')

        try:
            # Determine the padding width based on the longest repo_name
            max_repo_name_length = max(len(repo_name) for repo_name in self.manifest_repos)
            repo_num = 0

            for repo_name, repo in self.manifest_repos.items():
                if not isinstance(repo, dict):
                    self.log_fail(f"Repo '{repo_name}' is not a dictionary as expected.")

                repo_num += 1
                repo_stage_info = repo.get(self.manifest_stage) or self.get_fallback_stage_info()
                repo_checkout = repo_stage_info.get('checkout', 'Unknown')
                repo_checkout_type = repo_stage_info.get('checkout_type', 'Unknown')

                # Format the message with fixed width padding
                message = f"{repo_name:<{max_repo_name_length}} {repo_checkout} ({repo_checkout_type})"
                if self.manifest_is_dev_stage:
                    self.log_info(message)
                    continue

                # Production stage >> Additionally ensure that these are tagged with a version
                is_version_tag = repo_checkout_type == 'tag'
                if is_version_tag:
                    self.log_success(message)
                else:
                    self.log_warn(message)
        except AssertionError as e:
            self.log_fail(e)

        self.assert_complete()

    def assert_manifest_stage(self):
        self.log_test_name('assert_manifest_stage')

        try:
            manifest_stage = self.manifest['stage']
            expected = "manifest 'stage' == 'production_stage'"
            assert manifest_stage == "production_stage", \
                f"Expected {expected} [got '{manifest_stage}']"
            self.log_success(expected)
        except AssertionError as e:
            self.log_fail(e)
        self.assert_complete()

    # -- INIT --------------------------------------------------------------------------------------------- 

    # READONLY TESTER STARTS HERE >>
    def validate_files(self):
        """ Read-only checks to prep for production. """
        logging.info(f"{FYI_COLOR}Validating production stage ({self.manifest_target_prod_ver})...{Fore.RESET}")

        self.assert_manifest_stage()
        self.assert_manifest_repo_versions()
        self.assert_conf_dot_py()

    # WRITE TESTER STARTS HERE >>
    def set_production(self):
        """ (!) Changes files to set for production. """
        logging.info(f"Setting files for production using {self.repo_manifest_path}...")

    def run(self, dry_run, set_production):
        if dry_run:
            self.validate_files()
        elif set_production:
            self.set_production()
        else:
            logging.warning(WARN_COLOR + "Specify either --dry-run or --set-production")


def main():
    parser = argparse.ArgumentParser(description="Production Launch Checklist Tool")
    parser.add_argument('--dry-run', action='store_true', help="Perform a dry run")
    parser.add_argument('--set-production', action='store_true', help="Set files to production")

    args = parser.parse_args()

    prep = ProductionPrep()
    prep.run(args.dry_run, args.set_production)


if __name__ == "__main__":
    main()

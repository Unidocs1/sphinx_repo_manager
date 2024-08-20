""" Preps the project for production_stage. """
import argparse
import os
import yaml
from colorama import init, Fore, Style
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Define colors
ERR_COLOR = Fore.RED
WARN_COLOR = Fore.YELLOW

class ProductionPrep:
    def __init__(self):
        init(autoreset=True)  # Initialize colorama
        self.launch_path = os.getcwd()
        self.repo_manifest_path = os.path.abspath(os.path.join(self.launch_path, '../docs/repo_manifest.yml'))
        self.manifest = self.load_manifest()
        self.test_index = 0
    
    def get_test_index_str(self):
        return f"[{self.test_index}]"

    def load_manifest(self):
        """ Load the YAML manifest file and save it to self. """
        with open(self.repo_manifest_path, 'r') as file:
            return yaml.safe_load(file)
        
    def assert_manifest_stage(self):
        try:
            assert self.manifest['stage'] == "production_stage", "Expected manifest 'stage' is 'production_stage'"
        except AssertionError as e:
            logging.error(ERR_COLOR + str(e))

    def validate_files(self):
        """ Read-only checks to prep for production. """
        logging.info(f"Validating production stage...")
        
        self.assert_manifest_stage()

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

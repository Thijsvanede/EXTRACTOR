# Imports
import configparser

fpath = "./Data/lists.ini"

def load_lists(path):
    """Load lists from given file path."""
    # Initialise patterns
    patterns = {}

    # Initialise config parser
    config = configparser.ConfigParser()

    # Read file
    with open(path) as f:
        config.readfp(f)

    # Return result as dict
    return {type: config.get(type, 'pattern') for type in config.sections()}

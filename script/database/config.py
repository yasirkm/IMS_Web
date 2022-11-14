from pathlib import Path

from configparser import ConfigParser

POSTGRE_CONFIG_PATH=Path(__file__).parent / 'db.ini'

def postgre_config(filepath=POSTGRE_CONFIG_PATH, section='postgresql'):
    parser = ConfigParser()
    parser.read(filepath)

    db = {key:value for key, value in parser.items(section)}

    return db
from configparser import ConfigParser

def postgre_config(filename='db.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {key:value for key, value in parser.items(section)}

    return db
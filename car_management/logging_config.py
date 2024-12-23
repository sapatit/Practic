import logging
import logging.config
import yaml
import os


def setup_logging(config_file: str) -> None:
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f.read())

    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    config['loggers']['__main__']['level'] = log_level
    config['loggers']['statistics']['level'] = log_level

    logging.config.dictConfig(config)

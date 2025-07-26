# Enhanced logging setup
import logging

def setup_logging(log_file='financial_data_parser.log'):
    # Basic configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

setup_logging()

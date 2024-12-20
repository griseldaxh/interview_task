import logging
import os

def get_logger(name, log_file=None):
    """
    Configure and return a logger.

    :param name: Name of the logger.
    :param log_file: Optional path for the log file. Defaults to 'application.log' in the current working directory.
    :return: Configured logger object.
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times if logger already has them
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)  # Default log level

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # StreamHandler for console logging
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # FileHandler for file logging
        if log_file is None:
            log_file = os.path.join(os.getcwd(), "application.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
import logging

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.setup_logging()
        return cls._instance

    def setup_logging(self):
        """
        Sets up logging for the application.

        Attributes:
            logger (logging.Logger): The logger instance used to log messages from the
                application. Configured with file and stream handlers for logging.

        """
        self.logger = logging.getLogger(__name__)
        # Set the log level to INFO
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.INFO)  # Set log level for file handler to INFO
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)  # Set log level for stream handler to INFO
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger

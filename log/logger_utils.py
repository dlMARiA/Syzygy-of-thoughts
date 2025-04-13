import logging

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.setup_logging()
        return cls._instance

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)
        # 修改日志级别为 INFO
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.INFO)  # 设置文件处理器的日志级别为 INFO
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)  # 设置流处理器的日志级别为 INFO
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger
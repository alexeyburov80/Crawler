import logging

class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()  # вызываем метод flush(), а не присваиваем

# Использование
file_handler = FlushFileHandler("logs/crawler.log", mode="a", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)

logger = logging.getLogger("crawler")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
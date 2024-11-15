import logging
from logger import *

LEVEL_MAP = {
    logging.CRITICAL: LogLevel.ERROR,
    logging.FATAL: LogLevel.ERROR,
    logging.ERROR: LogLevel.ERROR,
    logging.WARNING: LogLevel.WARN,
    logging.WARN: LogLevel.WARN,
    logging.INFO: LogLevel.INFO,
    logging.DEBUG: LogLevel.DEBUG,
    logging.NOTSET: LogLevel.INFO,
}

class LoggingHandler(logging.Handler):
    

    def __init__(self, logger: Logger, level: Union[int, str] = logging.INFO):
        self.logger = logger
        super().__init__(level)
    
    def setLevel(self, level):
        super().setLevel(level)
        self.logger.enable_debug = self.level == logging.DEBUG


    def emit(self, record: logging.LogRecord):
        level = LEVEL_MAP[record.levelno]
        event = LogEvent(level, record.getMessage(), record.exc_info)
        self.logger._log(event)


if __name__ == "__main__":
    def bar():
        raise ValueError("meow")

    def foo():
        bar()
    l = Logger(debug=True)
    logging.basicConfig(level=logging.DEBUG, handlers=[LoggingHandler(l)])
    logging.info("Hello from logging")
    l.debug("Created logger")
    l.info("Hello world!")
    l.warn("Warn")
    l.error("Error!")
    try:
        foo()
    except Exception as e:
        l.error("Foo", e)
        l.warn(e)
        l.info(e)
        logging.error("LH e", exc_info=e)

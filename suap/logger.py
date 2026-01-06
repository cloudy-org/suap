import logging

__all__ = (
    "LogFormatter",
)

class LogFormatter(logging.Formatter):
    COLOURS = {
        logging.DEBUG: "\033[90m",
        logging.INFO: "\033[96m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
        logging.CRITICAL: "\033[95m",
    }

    def format(self, record):
        reset_colour = "\033[0m"

        colour = self.COLOURS.get(record.levelno, reset_colour)
        formatted_string = f"{colour}[%(levelname)s]{reset_colour}: %(message)s"

        return logging.Formatter(formatted_string).format(record)
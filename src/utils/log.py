import logging
from typing import Union
import warnings


class Log:
    loglevel = None
    root_logger = False
    logger = logging
    _log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @classmethod
    def set_up(cls, loglevel, root_logger=False):
        if root_logger:
            cls.root_logger = True
            logging.basicConfig(level=loglevel, format=cls._log_format)
        else:
            cls.logger = logging.getLogger("titanic-data-analysis")
            cls.logger.propagate = False
            cls.logger.setLevel(loglevel)
            cls.loglevel = loglevel
            ch = logging.StreamHandler()
            formatter = logging.Formatter(cls._log_format)
            ch.setFormatter(formatter)
            cls.logger.addHandler(ch)

    @classmethod
    def critical(cls, *msgs: any, return_code: Union[int, None] = 1):
        """
        Logs critical messages to stdout and exits program.
        :type msgs: object
        :param return_code: Override the return code or None to not exit program.
        """
        for msg in msgs:
            cls.logger.critical(msg)
        if return_code:
            exit(return_code)

    @classmethod
    def error(cls, *msgs: any, return_code: Union[int, None] = 1):
        """
        Logs error messages to stdout and exits program.
        :type msgs: object
        :param return_code: Override the return code or None to not exit program.
        """
        for msg in msgs:
            cls.logger.error(msg)
        if return_code:
            exit(return_code)

    @classmethod
    def warning(cls, *msgs: any):
        """
        Logs warning messages to stdout.
        :type msgs: object
        """
        for msg in msgs:
            cls.logger.warning(msg)

    @classmethod
    def warn(cls, *msgs: any):
        warnings.warn("The 'warn' function is deprecated, "
                      "use 'warning' instead", DeprecationWarning, 2)
        cls.warning(*msgs)

    @classmethod
    def info(cls, *msgs: any):
        """
        Logs info messages to stdout.
        :type msgs: object
        """
        for msg in msgs:
            cls.logger.info(msg)

    @classmethod
    def debug(cls, *msgs: any):
        """
        Logs debug messages to stdout.
        :type msgs: object
        """
        for msg in msgs:
            cls.logger.debug(msg)

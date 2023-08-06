"""Logging handlers, formatters and interfaces."""

import abc
import inspect
import logging
import logging.handlers
import sys
import queue
from contextvars import ContextVar  # noqa: pycharm
from typing import TypedDict, Union, Type, Tuple
from logging import DEBUG, INFO, WARNING, ERROR
from weakref import proxy

from kaiju_tools.registry import ClassRegistry
from kaiju_tools.encoding import SERIALIZERS
from kaiju_tools.exceptions import APIException, InternalError

__all__ = [
    'LogTrace',
    'LogException',
    'LogExceptionTrace',
    'LogMessage',
    'TextFormatter',
    'DataFormatter',
    'Adapter',
    'Logger',
    'StreamHandler',
    'QueueHandler',
    'FormatterInterface',
    'HandlerInterface',
    'Formatters',
    'Handlers',
    'FORMATTERS',
    'HANDLERS',
]


class LogTrace(TypedDict):
    """Log trace data."""

    path: str  #: full module path
    func: str  #: function name
    module: str  #: module name
    lineno: int  #: log record line number


class LogExceptionTrace(TypedDict):
    """Log exception trace and debug info."""

    stack: str  #: stack trace
    locals: dict  #: local variables
    lineno: int  #: exception line number


class LogException(TypedDict):
    """Log exc_info data."""

    cls: str  #: exception class name
    cls_full: str  #: full class name i.e. __qualname__
    message: str  #: exception message
    trace: Union[LogExceptionTrace, None]  #: stack trace data


class LogMessage(TypedDict):
    """Log message data."""

    timestamp: float  #: UNIX timestamp
    name: str  #: logger name
    level: str  #: log level
    message: str  #: log text message
    ctx: dict  #: context information (service variables, session data etc)
    data: dict  #: log message extras
    trace: LogTrace  #: log record trace information
    error: Union[LogException, None]  #: exc_info data


class _LogRecord(logging.LogRecord):
    _data: dict = None
    _cid: str = None
    _sid: str = None
    _dline: int = None

    @staticmethod
    def get_log_record(*args, **kws) -> '_LogRecord':
        """Get log record object."""
        return _LogRecord(*args, **kws)


class Logger(logging.Logger):
    """Main logger class."""

    def info(self, msg, /, *args, **kws) -> None:
        """INFO log."""
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, args, **kws)

    def debug(self, msg, /, *args, **kws) -> None:
        """DEBUG log."""
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, args, **kws)

    def error(self, msg, /, *args, **kws) -> None:
        """ERROR log."""
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, args, **kws)

    def warning(self, msg, /, *args, **kws) -> None:
        """WARNING log."""
        if self.isEnabledFor(WARNING):
            self._log(WARNING, msg, args, **kws)

    def _log(
        self,
        level,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1,
        _cid='',
        _sid=None,
        _dline=None,
        **kws,
    ):
        if extra is None:
            extra = {}
        extra['_data'] = kws
        extra['_cid'] = _cid
        extra['_sid'] = _sid
        extra['_dline'] = _dline
        super()._log(  # noqa: reasonable
            level=level,
            msg=msg,
            args=args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )


logging.setLoggerClass(Logger)
logging.setLogRecordFactory(_LogRecord.get_log_record)


class Adapter(logging.LoggerAdapter):
    """Logging adapter and log context manager.

    It is used to provide contextual information to log records.
    """

    def __init__(self, app, *args, **kws):
        super().__init__(*args, **kws)
        self._app = proxy(app)

    def process(self, msg: str, kwargs: dict) -> (str, dict):
        """Process the logging message and keyword arguments."""
        ctx = self._app.request_context.get()
        if ctx:
            kwargs['_cid'] = ctx['correlation_id']
            kwargs['_sid'] = ctx['session_id']
            kwargs['_dline'] = ctx['request_deadline']
        return msg, kwargs

    def getChild(self, suffix):  # noqa: python fails to follow the naming standards here
        """Get child logger.

        Compatibility method for `Logged` class.
        """
        return Adapter(self.logger.getChild(suffix), self.extra)


class FormatterInterface(logging.Formatter, abc.ABC):
    """Formatter base class."""


class TextFormatter(FormatterInterface):
    """Formatter for human-readable text."""

    COLORS = {
        'BLACK': '\033[30m',
        'RED': '\033[31m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[34m',
        'MAGENTA': '\033[35m',
        'CYAN': '\033[36m',
        'GRAY': '\033[37m',
        'UNDERLINE': '\033[4m',
        'RESET': '\033[0m',
    }

    COLOR_MAP = {
        logging.DEBUG: COLORS['GRAY'],
        logging.INFO: COLORS['RESET'],
        logging.WARNING: COLORS['YELLOW'],
        logging.ERROR: COLORS['RED'],
        logging.CRITICAL: COLORS['RED'],
    }

    default_date_fmt = '%H:%M:%S'
    default_log_fmt = '%(asctime)s | %(levelname)5s | %(_cid)s | %(name)s | %(message)s | %(_data)s'

    def __init__(
        self, *args, colored_mode: bool = False, datefmt: str = default_date_fmt, fmt: str = default_log_fmt, **kws
    ):
        """Initialize.

        :param colored_mode: output colored text depending on log level
        :param output_data: output log extra data
        :param output_context: output log adapter context data
        :param datefmt: log date format
        :param fmt: log format
        :param limit_var: limit variables in log in symbols
        :param args: see `logging.Formatter.__init__`
        :param kws: see `logging.Formatter.__init__`
        """
        super().__init__(*args, fmt=fmt, datefmt=datefmt, **kws)
        self.colored_mode = colored_mode

    def format(self, record):
        """Format log record."""
        msg = super().format(record)
        if self.colored_mode:
            self.set_color(record, msg)
        return msg

    @classmethod
    def set_color(cls, record, message: str) -> str:
        """Set message color according to log level."""
        color = cls.COLOR_MAP[record.levelno]
        msg = f'{color}{message}{cls.COLORS["RESET"]}'
        return msg


class DataFormatter(TextFormatter):
    """Colored formatter is used to pretty-print colored text in CLI.

    Text color depends on log level.
    """

    DEFAULT_ENCODING = 'application/json'

    def __init__(
        self,
        *args,
        debug: bool = False,
        encoder: str = DEFAULT_ENCODING,
        encoders=SERIALIZERS,
        **kws,
    ):
        """Initialize.

        :param debug: output debug information about exceptions
        :param encoder: data encoding format or encoder object itself or None for no additional encoding
        :param encoders: optional encoder classes registry
        :param args: see :py:class:`~kaiju_base.logging.TextFormatter`
        :param kws: see :py:class:`~kaiju_base.logging.TextFormatter`
        """
        super().__init__(*args, **kws)
        self._encoder = encoders[encoder]()
        self._debug = debug

    def format(self, record):
        """Format log record."""
        msg = self.create_message(record)  # noqa
        if self._encoder:
            msg = self._encoder.dumps(msg)
        else:
            msg = str(msg)
        if self.colored_mode:
            self.set_color(record, msg)
        return msg

    def formatMessage(self, record) -> str:
        """Format log message."""
        msg = self.create_message(record)  # noqa
        return str(msg)

    def formatException(self, ei):
        """Format exception (skip it)."""
        return

    def create_message(self, record: _LogRecord) -> LogMessage:
        """Create log message dict from a log record."""
        msg = {'t': record.created, 'name': record.name, 'lvl': record.levelname, 'msg': record.getMessage()}
        cid, sid, dline, data = record._cid, record._sid, record._dline, record._data  # noqa
        if cid:
            msg['cid'] = cid
        if sid:
            msg['sid'] = sid
        if dline:
            msg['t_max'] = dline
        if data:
            msg['data'] = data
        if record.exc_info:
            error_cls, error, stack = record.exc_info
            if not isinstance(error, APIException):
                error = InternalError(message=str(error), base_exc=error)
            error.debug = self._debug
            error.debug = True  # a little hack to enable trace info (probably there's a better way)
            if 'data' not in msg:
                msg['data'] = {}
            msg['data']['error'] = error.repr()
            error.debug = False
            if stack:
                msg['data']['error']['trace'] = {
                    'file': inspect.getabsfile(stack.tb_next),
                    'lineno': stack.tb_next.tb_lineno,
                }
        return msg  # noqa


class HandlerInterface(logging.Handler, abc.ABC):
    """Base log handler interface."""

    def __init__(self, app=None, **kws):
        """Initialize."""
        super().__init__(**kws)
        self.app = app


class StreamHandler(logging.StreamHandler, HandlerInterface):
    """Modified stream handler with `sys.stdout` by default."""

    stream_types = {'stdout': sys.stdout, 'stderr': sys.stderr}  #: available stream types

    def __init__(self, app=None, bytestream: bool = False, stream: str = None):
        """Initialize.

        If stream is not specified, `sys.stdout` is used.

        :param app: web app
        :param stream: optional stream type
        """
        if stream is None:
            stream = sys.stdout
        if bytestream:
            self.terminator: bytes = self.terminator.encode('utf-8')
            stream = stream.buffer
        elif isinstance(stream, str):
            stream = self.stream_types[stream]
        super().__init__(stream=stream)
        self.app = app


class QueueHandler(logging.handlers.QueueHandler, HandlerInterface):
    """Basic queue handler."""

    def __init__(self, app=None, **kws):
        """Initialize.

        :param app: web app
        :param kws: settings for the internal StreamHandler
        """
        q = queue.Queue(-1)
        super().__init__(q)
        self._stream = StreamHandler(app=app, **kws)
        self._listener = logging.handlers.QueueListener(q, self._stream)
        self._listener.start()
        self.app = app

    def setFormatter(self, fmt) -> None:
        self._stream.setFormatter(fmt)


class Formatters(ClassRegistry[str, Type[FormatterInterface]]):
    """Log formatter classes registry."""

    @classmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        return (FormatterInterface,)


class Handlers(ClassRegistry[str, Type[HandlerInterface]]):
    """Log handler classes registry."""

    @classmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        return (HandlerInterface,)


FORMATTERS = Formatters()
HANDLERS = Handlers()
FORMATTERS.register_from_namespace(locals())
HANDLERS.register_from_namespace(locals())

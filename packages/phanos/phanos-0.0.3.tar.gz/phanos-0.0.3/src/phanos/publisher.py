""" """
from __future__ import annotations
import logging
import sys
import threading
import typing
from abc import abstractmethod
from logging import Logger

import imp_prof.messaging.publisher

from imp_prof.messaging.publisher import BlockingPublisher

from .metrics import MetricWrapper, TimeProfiler, ResponseSize
from .tree import MethodTree


TIME_PROFILER = "time_profiler"
RESPONSE_SIZE = "response_size"


class OutputFormatter:
    """class for converting Record type into profiling string"""

    @staticmethod
    def record_to_str(name: str, record: imp_prof.Record) -> str:
        """converts Record type into profiling string

        :param name: name of profiler
        :param record: metric record which to convert
        """
        value = record["value"][1]
        if not record.get("labels"):
            return (
                f"profiler: {name}, "
                f"method: {record.get('method')}, "
                f"value: {value} {record.get('units')}"
            )
        # format labels as this "key=value, key2=value2"
        labels = ", ".join(f"{k}={v}" for k, v in record["labels"].items())
        return (
            f"profiler: {name}, "
            f"method: {record.get('method')}, "
            f"value: {value} {record.get('units')}, "
            f"labels: {labels}"
        )


class BaseHandler:
    """base class for record handling"""

    handler_name: str

    def __init__(self, handler_name: str) -> None:
        """
        :param handler_name: name of handler. used for managing handlers"""
        self.handler_name = handler_name

    @abstractmethod
    def handle(
        self, records: typing.List[imp_prof.Record], profiler_name: str = "profiler"
    ) -> None:
        """
        method for handling records

        :param profiler_name: name of profiler
        :param records: list of records to handle
        """
        raise NotImplementedError


class RabbitMQHandler(BaseHandler):
    """RabbitMQ record handler"""

    _publisher: BlockingPublisher
    _logger: logging.Logger

    def __init__(
        self,
        handler_name: str,
        host: str = "127.0.0.1",
        port: int = 5672,
        user: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        heartbeat: int = 47,
        timeout: float = 23,
        retry_delay: float = 0.137,
        retry: int = 3,
        exchange_name: str = "profiling",
        exchange_type: str = "fanout",
        logger: typing.Optional[Logger] = None,
        **kwargs,
    ) -> None:
        """Creates BlockingPublisher instance (connection not established yet),
         sets logger and create time profiler and response size profiler

        :param handler_name: name of handler. used for managing handlers
        :param host: RabbitMQ server host
        :param port: RabbitMQ server port
        :param user: RabbitMQ username
        :param password: RabbitMQ user password
        :param heartbeat:
        :param timeout:
        :param retry_delay:
        :param retry:
        :param exchange_name:
        :param exchange_type:
        :param logger: logger
        """
        super().__init__(handler_name)

        self._logger = logger or logging.getLogger(__name__)
        self._publisher = BlockingPublisher(
            host=host,
            port=port,
            user=user,
            password=password,
            heartbeat=heartbeat,
            timeout=timeout,
            retry_delay=retry_delay,
            retry=retry,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            logger=logger,
            **kwargs,
        )
        try:
            self._publisher.connect()
        except imp_prof.messaging.publisher.NETWORK_ERRORS as err:
            self._logger.error(
                f"RabbitMQHandler cannot connect to RabbitMQ because of {err}"
            )
            raise RuntimeError("Cannot connect to RabbitMQ") from err
        self._logger.info("RabbitMQHandler created successfully")
        self._publisher.close()

    def handle(
        self,
        records: typing.List[imp_prof.Record],
        profiler_name: str = "profiler",
    ) -> None:
        """Sends list of records to rabitMq queue

        :param profiler_name: name of profiler (not used)
        :param records: list of records to publish
        """

        _ = profiler_name
        for record in records:
            _ = self._publisher.publish(record)


class LoggerHandler(BaseHandler):
    """logger handler"""

    _logger: logging.Logger
    _formatter: OutputFormatter
    level: int

    def __init__(
        self,
        handler_name: str,
        logger: typing.Optional[logging.Logger] = None,
        level: int = 10,
    ) -> None:
        """

        :param handler_name: name of handler. used for managing handlers
        :param logger: logger instance if none -> creates new with name PHANOS
        :param level: level of logger in which prints records. default is DEBUG
        """
        super().__init__(handler_name)
        if logger is not None:
            self._logger = logger
        else:
            self._logger = logging.getLogger("PHANOS")
            self._logger.setLevel(10)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(10)
            self._logger.addHandler(handler)
        self.level = level
        self._formatter = OutputFormatter()

    def handle(
        self, records: typing.List[imp_prof.Record], profiler_name: str = "profiler"
    ) -> None:
        """logs list of records

        :param profiler_name: name of profiler
        :param records: list of records
        """
        for record in records:
            self._logger.log(
                self.level, self._formatter.record_to_str(profiler_name, record)
            )


class StreamHandler(BaseHandler):
    """Stream handler of Records."""

    _formatter: OutputFormatter
    output: typing.TextIO
    _lock: threading.Lock

    def __init__(self, handler_name: str, output: typing.TextIO = sys.stdout) -> None:
        """

        :param handler_name: name of profiler
        :param output: stream output. Default 'sys.stdout'
        """
        super().__init__(handler_name)
        self.output = output
        self._formatter = OutputFormatter()
        self._lock = threading.Lock()

    def handle(
        self, records: typing.List[imp_prof.Record], profiler_name: str = "profiler"
    ) -> None:
        """logs list of records

        :param profiler_name: name of profiler
        :param records: list of records
        """
        for record in records:
            with self._lock:
                print(
                    self._formatter.record_to_str(profiler_name, record),
                    file=self.output,
                    flush=True,
                )


class PhanosProfiler:
    """Class responsible for sending records to IMP_prof RabbitMQ publish queue"""

    _logger: Logger
    _metrics: typing.Dict[str, MetricWrapper]

    _root: MethodTree
    current_node: MethodTree

    time_profile: typing.Optional[TimeProfiler]
    resp_size_profile: typing.Optional[ResponseSize]

    before_func: typing.Optional[typing.Callable]
    after_func: typing.Optional[typing.Callable]
    before_root_func: typing.Optional[typing.Callable]
    after_root_func: typing.Optional[typing.Callable]

    _handlers: typing.Dict[str, BaseHandler]
    handle_records: bool

    def __init__(self) -> None:
        """Initialize ProfilesPublisher

        Initialization just creates new instance!!

        """

        self._metrics = {}
        self._handlers = {}

        self.request_size_profile = None
        self.time_profile = None

        self.before_func = None
        self.after_func = None
        self.before_root_func = None
        self.after_root_func = None

    def config(
        self,
        logger=None,
        time_profile: bool = True,
        request_size_profile: bool = True,
        handle_records: bool = True,
    ) -> None:
        """configure PhanosProfiler
        :param logger: logger instance
        :param time_profile: should create instance time profiler
        :param request_size_profile: should create instance of request size profiler
        :param handle_records: should handle recorded records
        """
        self._logger = logger or logging.getLogger(__name__)
        if time_profile:
            self.create_time_profiler()
        if request_size_profile:
            self.create_response_size_profiler()
        self.handle_records = handle_records

        self._root = MethodTree(None, self._logger)
        self.current_node = self._root

    def create_time_profiler(self) -> None:
        """Create time profiling metric"""
        self.time_profile = TimeProfiler(TIME_PROFILER, logger=self._logger)
        self.add_metric(self.time_profile)
        self._logger.debug("Phanos - time profiler created")

    def create_response_size_profiler(self) -> None:
        """create response size profiling metric"""
        self.resp_size_profile = ResponseSize(RESPONSE_SIZE, logger=self._logger)
        self.add_metric(self.resp_size_profile)
        self._logger.debug("Phanos - response size profiler created")

    def delete_metric(self, item: str) -> None:
        """deletes one metric instance
        :param item: name of the metric instance
        """
        _ = self._metrics.pop(item, None)
        if item == "time_profiler":
            self.time_profile = None
        if item == "response_size":
            self.resp_size_profile = None
        self._logger.debug(f"Phanos - metric {item} deleted")

    def delete_metrics(
        self, rm_time_profile: bool = False, rm_resp_size_profile: bool = False
    ) -> None:
        """deletes all custom metric instances

        :param rm_time_profile: should pre created time_profiler be deleted
        :param rm_resp_size_profile: should pre created response_size_profiler be deleted
        """
        names = list(self._metrics.keys())
        for name in names:
            if (name != TIME_PROFILER or rm_time_profile) and (
                name != RESPONSE_SIZE or rm_resp_size_profile
            ):
                self.delete_metric(name)

    def clear(self):
        """clear all records from all metrics and clear method tree"""
        for metric in self._metrics.values():
            metric.cleanup()

        self.current_node = self._root
        self._root.clear_tree()

    def add_metric(self, metric: MetricWrapper) -> None:
        """adds new metric to profiling

        :param metric: metric instance
        """
        self._metrics[metric.name] = metric
        self._logger.debug(f"Phanos - metric {metric.name} added")

    def add_handler(self, handler: BaseHandler) -> None:
        """Add handler to profiler

        :param handler: handler instance
        """
        self._handlers[handler.handler_name] = handler
        self._logger.debug(f"Handler {handler.handler_name} added to phanos profiler")

    def delete_handler(self, handler_name: str) -> None:
        """Delete handler from profiler

        :param handler_name: name of handler:
        """
        _ = self._handlers.pop(handler_name, None)
        self._logger.debug(f"Phanos - handler {handler_name} deleted")

    def delete_handlers(self) -> None:
        """delete all handlers"""
        self._handlers.clear()
        self._logger.debug(f"Phanos - All handlers deleted")

    def profile(self, func: typing.Callable) -> typing.Callable:
        """
        Decorator specifying which methods should be profiled.
        Default profiler is time profiler which measures execution time of decorated methods

        Usage: decorate methods which you want to be profiled

        :param func: method or function which should be profiled
        """

        def inner(*args, **kwargs) -> typing.Any:
            if self._handlers and self.handle_records:
                self.current_node = self.current_node.add_child(
                    MethodTree(func, self._logger)
                )

                if self.current_node.parent == self._root:
                    self._logger.debug(f"Phanos - before root execution")
                    self._before_root_func(*args, **kwargs)
                self._logger.debug(f"Phanos - before func execution")
                self._before_func(*args, **kwargs)

            result = func(*args, **kwargs)

            if self._handlers and self.handle_records:
                self._logger.debug(f"Phanos - after func execution")
                self._after_func(*args, **kwargs)

                if self.current_node.parent == self._root:
                    self._logger.debug(f"Phanos - after root execution")
                    self._after_root_func(*args, **kwargs)
                    self.handle_records_clear()

                self.current_node = self.current_node.parent
                self.current_node.delete_child()
            return result

        return inner

    def _before_root_func(self, function: typing.Callable, *args, **kwargs) -> None:
        """method executing before root function

        :param function: root function
        """
        # custom
        if callable(self.before_root_func):
            self.before_root_func(function=function, *args, **kwargs)
        # here mine if needed

    def _after_root_func(self, fn_result: typing.Any, *args, **kwargs) -> None:
        """method executing after the root function


        :param fn_result: result of function
        """
        # mine
        if self.resp_size_profile:
            self.resp_size_profile.store_operation(
                operation="rec",
                method=self.current_node.context,
                value=fn_result,
                label_values={},
            )
        # user custom function
        if callable(self.after_root_func):
            self.after_root_func(fn_result=fn_result, *args, **kwargs)

    def _before_func(self, func, *args, **kwargs) -> None:
        # user custom
        if callable(self.before_func):
            self.before_func(function=func, *args, **kwargs)
        # mine
        if self.time_profile:
            self.time_profile.start()

    def _after_func(self, fn_result: typing.Any, *args, **kwargs) -> None:
        # mine
        if self.time_profile:
            self.time_profile.store_operation(
                operation="stop", method=self.current_node.context, label_values={}
            )
            self._logger.debug(f"Phanos - {self.time_profile.name} recorded operation ")
        # custom
        if callable(self.after_func):
            self.after_func(fn_result=fn_result, *args, **kwargs)

    def handle_records_clear(self) -> None:
        """Pass records to each registered Handler and clear stored records"""
        # send records and log em
        for metric in self._metrics.values():
            records = metric.to_records()
            for handler in self._handlers.values():
                self._logger.debug(
                    f"Phanos - handler {handler.handler_name} handling metric {metric.name}"
                )
                handler.handle(records, metric.name)
            metric.cleanup()

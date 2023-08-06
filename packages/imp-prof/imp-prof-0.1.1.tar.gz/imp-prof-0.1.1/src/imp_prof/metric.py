import gzip
import os
import typing
from enum import Enum

import fastapi
import prometheus_client as prometheus
from starlette.requests import Request
from starlette.responses import Response

from . import types

DEFAULT_LABELS = {
    "job",
    "method",
}

BUCKETS_LATENCY: typing.Sequence[float] = (
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.2,
    0.2,
    0.3,
    0.4,
    0.5,
    0.75,
    1,
    1.5,
    2,
    2.5,
    3,
    3.5,
    4,
    4.5,
    5,
    7.5,
    10,
    15,
    20,
    30,
    60,
)


def metric_name(item: str, metric: str, units: str) -> str:
    return f"{item}_{metric}_{units}"


M = typing.TypeVar("M", bound=prometheus.metrics.MetricWrapperBase)


class MetricWriter(typing.Generic[M]):
    """Wraps particular metric to provide unify interface. You can add new metrics with `register` class method"""

    DEFAULT_OPERATIONS: typing.ClassVar[typing.Dict[typing.Type[prometheus.metrics.MetricWrapperBase], str]] = {
        prometheus.Histogram: "observe",
        prometheus.Summary: "inc",
        prometheus.Counter: "inc",
        prometheus.Info: "info",
        prometheus.Gauge: "inc",
        prometheus.Enum: "state",
    }
    _metric: M
    _default_method: str

    __slots__ = (
        "_metric",
        "_default_method",
    )

    @classmethod
    def register(
        cls,
        type_: typing.Type[prometheus.metrics.MetricWrapperBase],
        method: typing.Union[typing.Callable, str] = "inc",
    ) -> None:
        """
        Register new metric type to be wrapp-able with this class.

        :param type_: metric class
        :param method: method or name of method to call when adding new record to metric instance
        """
        if not callable(method):
            raise TypeError("'method' has to be str or callable")
        cls.DEFAULT_OPERATIONS[type_] = str(getattr(method, "__name__", method))

    def __init__(self, metric: M) -> None:
        """
        Wrap metric to unify write.

        :param metric: wrapped metric
        """
        self._metric = metric
        self._default_method = self.DEFAULT_OPERATIONS[type(metric)]

    @property
    def metric(self) -> M:
        return self._metric

    def write(
        self,
        labels: typing.Dict[str, str],
        value: typing.Any,
        method: typing.Optional[str] = None,
    ) -> None:
        """
        Unify method to write value into metric.

        :param labels: use these labels
        :param value: write this value
        :param method: call this method of metric, if not given `self._method_name`
        """
        _ = getattr(
            self._metric.labels(**labels),
            method or self._default_method,
        )(value)


class Recorder:
    """
    Dynamically creates metrics based on required records and is able to export metrics.
    Instance is ready to be exposed to FastApi app with `expose` method.
    You can add new metrics with `register` method.
    """

    METRIC_TYPES: typing.ClassVar[typing.Dict[str, typing.Type[prometheus.metrics.MetricWrapperBase]]] = {
        "histogram": prometheus.Histogram,
        "summary": prometheus.Summary,
        "counter": prometheus.Counter,
        "info": prometheus.Info,
        "gauge": prometheus.Gauge,
        "enum": prometheus.Enum,
    }

    @classmethod
    def register(
        cls,
        name: str,
        type_: typing.Type[prometheus.metrics.MetricWrapperBase],
    ) -> None:
        """
        Register new metric to be recorded by instances of this class.

        :param name: name used in record
        :param type_: constructor of new metric
        """
        cls.METRIC_TYPES[name] = type_

    __slots__ = (
        "items_metrics",
        "registry",
    )

    items_metrics: dict[str, dict[str, MetricWriter]]
    registry: prometheus.CollectorRegistry

    def __init__(self, auto_describe: bool = True) -> None:
        """Composite metrics with registry to export them."""
        self.items_metrics = {}  # histogram = items_metrics[item]["histogram"]
        self.registry = prometheus.CollectorRegistry(auto_describe=auto_describe)

    def new_metric(
        self,
        pattern: types.Record,
        name: typing.Optional[str] = None,
    ) -> MetricWriter:
        """
        Creates new metric object linked to `self.registry` of this recorder.

        :param pattern: create metric for this type of record
        :param name: if not given pattern["metric"].lower() is used
        :return: new instance
        """
        metric = name or pattern["metric"].lower()
        metric_cls = type(self).METRIC_TYPES.get(metric)
        if not metric_cls:
            raise ValueError(f"{type(self).__qualname__} - unknown metric: {metric!r}")
        optionals = {"buckets": BUCKETS_LATENCY} if metric == "histogram" else {}
        label_names = tuple(pattern["labels"].keys()) if pattern["labels"] else tuple()
        label_names += ("job", "method",)
        return MetricWriter(
            metric=metric_cls(
                name=metric_name(pattern["item"], metric, pattern["units"]),
                documentation=f'{metric} of {pattern["item"]} in {pattern["units"]}',
                labelnames=label_names,
                registry=self.registry,
                **optionals,
            )
        )

    def _create_and_bind_metric(
        self,
        pattern: types.Record,
    ) -> None:
        """
        Create or override metric based on given example record. New metric is part of `self.registry`.
        New metric is placed into `self.items_metrics`
        :param pattern: use this record as pattern of whole metric
        """
        if pattern["item"] not in self.items_metrics:
            self.items_metrics[pattern["item"]] = {}
        metric_name_ = pattern["metric"].lower()
        new_metric = self.new_metric(pattern, name=metric_name_)
        self.items_metrics[pattern["item"]][metric_name_] = new_metric

    def get_metric(
        self,
        item: str = "",
        metric: str = "",
    ) -> MetricWriter:
        """Find matching metric in `self.items_metrics`."""
        return self.items_metrics[item][metric]

    def has_metric(
        self,
        item: str = "",
        metric: str = "",
    ) -> bool:
        return item in self.items_metrics and metric in self.items_metrics[item]

    def metric_for(
        self,
        pattern: types.Record,
    ) -> MetricWriter:
        """
        Get cached or create new record pattern for given record.

        :param pattern: record example
        :return: metric writer
        """
        if not self.has_metric(pattern["item"], pattern["metric"]):
            self._create_and_bind_metric(pattern=pattern)
        return self.get_metric(pattern["item"], pattern["metric"])

    def write(
        self,
        new: types.Record,
    ) -> bool:
        """
        Note one record. If there is no matching metrics for `{item}_{metric}_{units}` new one is created.

        :param new: new data to record
        :return: True if record is valid; False if record is skipped
        """
        labels = {
            "job": new["job"],
            "method": new["method"],
            **(new["labels"] if new["labels"] else {}),
        }
        target_metric = self.metric_for(new)
        try:
            if isinstance(new["value"], (float, str)):
                target_metric.write(labels, new["value"])
            else:
                target_metric.write(labels, new["value"][1], method=new["value"][0])
        except AttributeError:
            return False
        return True

    def expose(
        self,
        app: fastapi.FastAPI,
        should_gzip: bool = False,
        endpoint: str = "/metrics",
        include_in_schema: bool = True,
        tags: typing.Optional[list[typing.Union[str, Enum]]] = None,
        **kwargs,
    ) -> "Recorder":
        """Exposes endpoint for metrics.

        :param app: FastAPI app instance. Endpoint will be added to this app.
        :param should_gzip: Should the endpoint return compressed data? It will
                also check for `gzip` in the `Accept-Encoding` header.
                Compression consumes more CPU cycles. In most cases it's best
                to just leave this option off since network bandwidth is usually
                cheaper than CPU cycles. Defaults to `False`.
        :param endpoint: Endpoint on which metrics should be exposed.
        :param include_in_schema: Should the endpoint show up in the documentation?
        :param tags: If you manage your routes with tags.
                Defaults to None.
        :param kwargs: Will be passed to FastAPI route annotation.
        :raises: ValueError: If `prometheus_multiproc_dir` env var is found but
                doesn't point to a valid directory.
        :returns: self: Recorder. Builder Pattern.
        """
        from prometheus_client import (
            CONTENT_TYPE_LATEST,
            REGISTRY,
            CollectorRegistry,
            generate_latest,
            multiprocess,
        )

        if "prometheus_multiproc_dir" in os.environ:
            pmd = os.environ["prometheus_multiproc_dir"]
            if not os.path.isdir(pmd):
                raise ValueError(f"Env var prometheus_multiproc_dir='{pmd}' not a directory.")
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry)
        else:
            registry = self.registry or REGISTRY

        @app.get(endpoint, include_in_schema=include_in_schema, tags=tags, **kwargs)
        async def metrics(request: Request):
            """Endpoint that serves Prometheus metrics."""
            if should_gzip and "gzip" in request.headers.get("Accept-Encoding", ""):
                resp = Response(content=gzip.compress(generate_latest(registry)))
                resp.headers["Content-Type"] = CONTENT_TYPE_LATEST
                resp.headers["Content-Encoding"] = "gzip"
            else:
                resp = Response(content=generate_latest(registry))
                resp.headers["Content-Type"] = CONTENT_TYPE_LATEST
            return resp

        return self

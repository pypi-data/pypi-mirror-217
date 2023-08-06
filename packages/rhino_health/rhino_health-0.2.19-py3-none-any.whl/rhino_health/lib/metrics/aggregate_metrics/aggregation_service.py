from itertools import chain
from typing import Callable, List, Optional

from funcy import compact

from rhino_health.lib.metrics.aggregate_metrics.aggregation_configuration import (
    SUPPORTED_AGGREGATE_METRICS,
)
from rhino_health.lib.metrics.aggregate_metrics.aggregation_constants import (
    AGGREGATION_METHOD,
    COUNT_VARIABLE_NAME,
    METRIC_FETCHER,
)
from rhino_health.lib.metrics.aggregate_metrics.aggregation_data_fetchers import (
    DefaultMetricFetcher,
    MetricFetcher,
)
from rhino_health.lib.metrics.aggregate_metrics.aggregation_methods import weighted_average
from rhino_health.lib.metrics.base_metric import MetricResponse, MetricResultDataType


def get_aggregate_metric_data(session, cohort_uids, metric_configuration) -> List[MetricResponse]:
    """
    Fetches data for aggregate metrics from multiple sources
    """
    metric = metric_configuration.metric_name()
    if metric not in SUPPORTED_AGGREGATE_METRICS:
        raise ValueError("Unsupported metric for aggregation")
    aggregation_configuration = SUPPORTED_AGGREGATE_METRICS[metric]
    metric_fetcher: MetricFetcher = aggregation_configuration.get(
        METRIC_FETCHER, DefaultMetricFetcher()
    )
    return metric_fetcher.fetch_metrics(session, cohort_uids, metric_configuration)


def calculate_aggregate_metric(
    metric_configuration,
    metric_results: List[MetricResultDataType],
    aggregation_method_override: Optional[Callable] = None,
) -> MetricResultDataType:
    """
    Aggregates the results from the individual cohorts into one.
    """
    metric = metric_configuration.metric_name()
    if metric not in SUPPORTED_AGGREGATE_METRICS:
        raise ValueError("Unsupported metric for aggregation")
    aggregation_configuration = SUPPORTED_AGGREGATE_METRICS[metric]
    aggregation_method = aggregation_method_override or aggregation_configuration.get(
        AGGREGATION_METHOD, weighted_average
    )
    count_variable = aggregation_configuration.get(COUNT_VARIABLE_NAME, "variable")
    if metric_configuration.group_by is None:
        return aggregation_method(metric, metric_results, count_variable=count_variable)
    else:
        # We get the unique group names from the data to iterate over since not all sites have all groups
        groups = set(chain.from_iterable(metric_result.keys() for metric_result in metric_results))
        grouped_results = {}
        for group in groups:
            group_result = compact(
                [metric_result.get(group, None) for metric_result in metric_results]
            )
            grouped_results[group] = aggregation_method(
                metric, group_result, count_variable=count_variable
            )
        return grouped_results
